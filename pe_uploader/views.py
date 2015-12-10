import os
import re
from functools import wraps

from flask import request, redirect, url_for, render_template, \
    send_from_directory, flash, jsonify, session, g
from pe_uploader import app, db
from pe_uploader.models import Files, User
from pe_uploader.forms import LoginForm
# from werkzeug import secure_filename


def secure_filename(name):
    # 2個以上の.と0個以上の/を置き換え置換
    name = re.sub(r'\.{2}\/', "", name)
    return name.replace(" ", "_")  # 空白をアンダースコアに置換


def login_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_view


@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(session['user_id'])


@app.route('/')
def list_files():
    files = Files.query.order_by(Files.id.desc()).all()
    files = reversed(files)
    return render_template('list_files.html', files=files, user=g.user)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# 与えられたfilenameを現在時刻とハッシュ化して返す
def hashed_filename(filename):
    import datetime
    import hashlib

    ext = "." + filename.rsplit('.', 1)[1]
    now = datetime.datetime.today()
    now = now.strftime("%Y/%m/%d-%H:%M:%S:%f")
    hashed = now + filename
    return hashlib.sha1(hashed.encode()).hexdigest() + ext


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        fileobj = request.files['file']
        if fileobj:
            if allowed_file(fileobj.filename):
                filename_raw = secure_filename(fileobj.filename)  # 生のファイル名
                filename_hashed = hashed_filename(filename_raw)   # ハッシュ化されたファイル名
                # 保存先はハッシュ化されたファイルパスを選択する必要がある
                filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                        filename_hashed)
                fileobj.save(filepath)
                # Register db
                file = Files(name=filename_raw, hashed=filename_hashed,
                             path="files/" + filename_hashed)
                db.session.add(file)
                db.session.commit()
                flash('<div class="alert alert-success" role="alert">Successfly upload file</div>')
                # return redirect(url_for('uploaded_file', filename=filename))
                return redirect(url_for('list_files'))
            else:
                flash('<div class="alert alert-danger" role="alert">Your file type is NOT allowd.</div>')
                return redirect(url_for('upload_file'))
        flash('<div class="alert alert-info" role="alert">No file uploaded.</div>')
        return redirect(url_for('upload_file'))
    return render_template('upload.html')


# 実際にファイルをみる
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ファイルを削除する
@app.route('/files/<filehashed>/delete', methods=['DELETE'])
@login_required
def delete_file(filehashed):
    file = Files.query.filter(Files.hashed == filehashed).first()
    if file is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.hashed))  # ファイルを削除
    db.session.delete(file)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user, authenticated = User.authenticate(db.session.query,
                                                form.name.data,
                                                form.password.data)
        if authenticated:
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('<div class="alert alert-success" role="alert">You were logged in</div>')
            return redirect(url_for('list_files'))
        else:
            flash('<div class="alert alert-danger" role="alert">Invalid user or password</div>')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('<div class="alert alert-success" role="alert">You were logged out</div>')
    return redirect('/')


@app.route('/admin/add', methods=["GET", "POST"])
def add_admin():
    admin = User.query.get(1)
    if admin is None:
        # Adminを作成する
        if request.method == 'POST':
            admin = User(name=request.form['name'],
                         password=request.form['password'])
            db.session.add(admin)
            db.session.commit()
            flash('<div class="alert alert-success" role="alert">Successfly add your admin user</div>')
            return redirect(url_for('login'))
        else:
            return render_template('admin/add.html')
    return redirect(url_for('edit_admin'))


# パスワードとユーザー名を変更する
@app.route('/admin/edit', methods=["GET", "POST"])
@login_required
def edit_admin():
    admin = User.query.get(1)
    if admin is None:
        return redirect(url_for('add_admin'))
    if request.method == 'POST':
        if request.form['name']:
            admin.name = request.form['name']
            f = "Change username"
        if request.form['password']:
            admin.password = request.form['password']
            f = "Change password"
        db.session.commit()
        flash('<div class="alert alert-success" role="alert">{}</div>'.format(f))
        return redirect(url_for('logout'))
    return render_template('admin/edit.html', user=admin)
