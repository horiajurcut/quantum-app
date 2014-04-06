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
    page = db.session.query(Page).filter(
        page_id == page_id
    ).first()

    events = db.session.query(Event).filter(
        Event.page_id == page.id
    ).all()

    return render_template('listing.html', events=events, page_id=page_id)


@app.route('/dashboard/event/<event_id>')
def dashboard_event(event_id):
    return render_template('dashboard.html')


@app.route('/dashboard/event/<event_id>/delete')
def dashboard_delete(event_id):
    event = db.session.query(Event).filter(
        Event.id == event_id
    ).first()

    page = db.session.query(Page).filter(
        Page.id == event.page_id
    ).first()

    db.session.delete(event)
    db.session.commit()

    return redirect('/dashboard/page/%s' % page.page_id)


@app.route('/dashboard/new', methods=['POST'])
def dashboard_new():
    form = request.form

    page_id = form['session-page']

    page = db.session.query(Page).filter(
        page_id == page_id
    ).first()

    new_event = {
        'page_id': page.id,
        'title': form['session-title'],
        'message': 'This is a random message'
    }

    if form['session-start-date']:
        new_event['start_date'] = datetime.datetime.strptime(form['session-start-date'], '%Y\/%m//%d %H:%M')

    if form['session-end-date']:
        new_event['end_date'] = datetime.datetime.strptime(form['session-end-date'], '%Y\/%m/\%d %H:%M')

    db_event = Event(**new_event)

    db.session.add(db_event)
    db.session.commit()

    return redirect('/dashboard/page/%s' % page_id)


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
