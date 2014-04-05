from flask import Flask
from flask import render_template

from api.core import app

@app.route('/dashboard')
def dashboard():
    users = db.session.query(User).all()
    return render_template('dashboard.html')