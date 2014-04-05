from flask import Flask
from flask import Response
from flask import request
from flask import render_template

from api.core import app, db
from api.models.user import User

import json

@app.route('/dashboard')
def dashboard():
    users = db.session.query(User).all()

    sentence = "At eight o'clock on Thursday morning, Arthur didn't feel very good."

    return Response(json.dumps({
        'users': [u.serialize for u in users]
    }), mimetype='application/json')
