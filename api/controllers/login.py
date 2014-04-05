from flask import Flask
from flask import session
from flask import Response
from flask import request
from flask import redirect, url_for
from flask import render_template

from api.core import app

import urllib
import json

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/auth/<token>')
def get_token(token):
    params = {
        'access_token': token
    }
    params = urllib.urlencode(params)
    accounts = json.loads(urllib.urlopen('https://graph.facebook.com/me/accounts?%s' % params).read())

    if 'data' not in accounts:
        return redirect('/')

    if len(accounts) > 1:
        return render_template('chooser.html', pages=accounts['data'])

    return Response(json.dumps({
        'accounts': accounts
    }), mimetype='application/json')
