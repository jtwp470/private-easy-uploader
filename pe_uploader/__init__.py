from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.debug = True
app.config.from_object('pe_uploader.config')

db = SQLAlchemy(app)

import pe_uploader.views
