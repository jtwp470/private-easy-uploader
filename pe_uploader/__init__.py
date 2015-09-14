from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os


UPLOAD_FOLDER = os.path.dirname(__file__) + "/files"  # 絶対パス
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.debug = True
app.config.from_object('pe_uploader.config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

db = SQLAlchemy(app)

import pe_uploader.views
