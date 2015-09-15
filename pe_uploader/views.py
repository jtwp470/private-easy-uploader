import os
from flask import request, redirect, url_for, render_template, \
    send_from_directory, flash, jsonify
from pe_uploader import app, db
from pe_uploader.models import Files
from werkzeug import secure_filename


@app.route('/')
def list_files():
    files = Files.query.order_by(Files.id.desc()).all()
    print(files)
    return render_template('list_files.html', files=files)


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
def upload_file():
    if request.method == 'POST':
        fileobj = request.files['file']
        if fileobj and allowed_file(fileobj.filename):
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
        flash('<div class="alert alert-info" role="alert">No file uploaded.</div>')
        return redirect(url_for('list_files'))
    return render_template('upload.html')


# 実際にファイルをみる
@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ファイルを削除する
@app.route('/files/<filehashed>/delete', methods=['DELETE'])
def delete_file(filehashed):
    file = Files.query.filter(Files.hashed == filehashed).first()
    if file is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filehashed))  # ファイルを削除
    db.session.delete(file)
    db.session.commit()
    return jsonify({'status': 'OK'})
