from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+gaerdbms:///quantum?instance=quantum-app-sw:qa'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:dordevama@localhost/quantum'

db = SQLAlchemy(app)
