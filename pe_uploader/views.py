from flask import request, redirect, url_for, render_template, flash
from pe_uploader import app, db
from pe_uploader.models import Files


@app.route('/')
def list_files():
    files = Files.query.order_by(Files.id.desc()).all()
    return render_template('list_files.html', files=files)
