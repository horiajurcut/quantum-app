from flask import Flask
from flask import session
from flask import Response
from flask import request
from flask import redirect, url_for
from flask import render_template

from api.core import app, db
from api.models.user import User
from api.models.page import Page
from api.models.event import Event

import urllib
import json
import datetime


@app.route('/dashboard/page/<page_id>')
def dashboard_page(page_id):
    return render_template('new.html')


@app.route('/dashboard/new', methods=['POST'])
def dashboard_new():
    form = request.data

    new_event = {
        'title': form['title'],
        'message': 'This is a random message',
        'start_date': datetime.datetime.now(),
        'end_date': datetime.datetime.now()
    }

    db_event = Event(**new_event)

    db.session.add(db_event)
    db.session.commit()


@app.route('/dashboard/page/<page_id>/<access_token>')
def dashboard_page_token(page_id, access_token):
    fb_page = {
        'user_id': session['USER_ID'],
        'page_id': page_id,
        'token': access_token
    }

    db_page = db.session.query(Page).filter(
        Page.page_id == page_id
    ).first()

    if not db_page:
        db_page = Page(**fb_page)

        db.session.add(db_page)
        db.session.commit()

    return redirect('/dashboard/page/%s' % page_id)


@app.route('/dashboard')
def dashboard():
    users = db.session.query(User).all()

    sentence = "At eight o'clock on Thursday morning, Arthur didn't feel very good."

    return Response(json.dumps({
        'users': [u.serialize for u in users]
    }), mimetype='application/json')
