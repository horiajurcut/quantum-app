from flask import Flask
from flask import session
from flask import Response
from flask import request
from flask import redirect, url_for
from flask import render_template

from api.core import app, db
from api.models.user import User
from api.models.page import Page

import urllib
import json
import datetime
import subprocess


@app.route('/github', methods=['POST'])
def github():
    payload = request.data

    if payload:
        subprocess.call(['./deploy.sh'])

