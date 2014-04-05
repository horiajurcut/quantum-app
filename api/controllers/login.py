from flask import Flask
from flask import render_template

from api.core import app

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chooser')
def chooser():
    return render_template('chooser.html')