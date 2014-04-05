from flask import Flask
from flask import render_template

from api.core import app

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
