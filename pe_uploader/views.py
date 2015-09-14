import os
from flask import request, redirect, url_for, render_template, \
    send_from_directory
from pe_uploader import app, db
from pe_uploader.models import Files
from werkzeug import secure_filename


@app.route('/')
def list_files():
    files = Files.query.order_by(Files.id.desc()).all()
    return render_template('list_files.html', files=files)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        fileobj = request.files['file']
        path = "{upload}/{name}".format(
            upload=app.config['UPLOAD_FOLDER'], name=fileobj.filename)
        if fileobj and allowed_file(fileobj.filename):
            filename = secure_filename(fileobj.filename)
            fileobj.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Register db
            file = Files(name=fileobj.filename, path=path)
            print(file)
            db.session.add(file)
            db.session.commit()
            # return redirect(url_for('uploaded_file', filename=filename))
        return redirect(url_for('list_files'))
    return render_template('upload.html')


# 実際にファイルをアップロードするところ
@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# 各ファイルの情報を見る
@app.route('/files/<int:file_id>/')
def show_files(file_id):
    return NotImplementedError()
