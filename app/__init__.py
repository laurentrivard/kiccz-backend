from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import UPLOAD_FOLDER
import os

app = Flask(__name__, static_url_path = '/static', static_folder="static")
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

from app import views, models

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('microblog startup')