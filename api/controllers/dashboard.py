from flask import Flask
from flask import render_template

from api.core import app

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html', name='Horia')
