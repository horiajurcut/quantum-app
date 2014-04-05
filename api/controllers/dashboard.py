from flask import Flask
from flask import render_template

from api.core import app, db
from api.models.user import User

@app.route('/')
def hello():
    users = db.session.query(User).all()

    return render_template('index.html', name='Horia')
