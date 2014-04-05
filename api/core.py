from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:okidoki1?localhost/quantum'

db = SQLAlchemy(app)