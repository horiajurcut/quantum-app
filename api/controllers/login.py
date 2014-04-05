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

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/auth/<token>')
def get_token(token):
    params = {
        'access_token': token
    }
    params = urllib.urlencode(params)

    me = json.loads(urllib.urlopen('https://graph.facebook.com/me?%s' % params).read())

    fb_user = {
        'first_name': me['first_name'],
        'last_name':  me['last_name'],
        'fb_id':      me['id'],
        'email':      me['email'],
        'created':    datetime.datetime.now()
    }

    db_user = db.session.query(User).filter(
        User.fb_id == fb_user['fb_id']
    ).first()

    if not db_user:
        db_user = User(**fb_user)

        db.session.add(db_user)
        db.session.commit()

    session['USER_ID'] = db_user.id

    accounts = json.loads(urllib.urlopen('https://graph.facebook.com/me/accounts?%s' % params).read())

    if 'data' not in accounts:
        return redirect('/')

    if len(accounts) > 1:
        return render_template('chooser.html', pages=accounts['data'])

    return Response(json.dumps({
        'accounts': accounts
    }), mimetype='application/json')
