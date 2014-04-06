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
from api.models.question import Question
from api.models.group import Group

from api.controllers.nlp import *

import urllib
import requests
import json
import datetime

from gensim import corpora, models, similarities


@app.route('/dashboard/page/<page_id>')
def dashboard_page(page_id):
    page = db.session.query(Page).filter(
        Page.page_id == page_id
    ).first()

    events = db.session.query(Event).filter(
        Event.page_id == page.id
    ).all()

    return render_template('listing.html', events=events, page_id=page_id)


@app.route('/dashboard/event/<event_id>')
def dashboard_event(event_id):
    event = db.session.query(Event).filter(
        Event.id == event_id
    ).first()

    page = db.session.query(Page).filter(
        Page.id == event.page_id
    ).first()

    return render_template('dashboard.html', page_id=page.page_id)


@app.route('/dashboard/event/<event_id>/retrieve')
def dashboard_retrieve(event_id):
    event = db.session.query(Event).filter(
        Event.id == event_id
    ).first()

    if event.fb_post_id is None:
        return Response(json.dumps({
            'questions': []
        }), mimetype='application/json')


    page = db.session.query(Page).filter(
        Page.id == event.page_id
    ).first()

    params = {
        'access_token': page.token
    }
    params = urllib.urlencode(params)
    questions = json.loads(
        urllib.urlopen('https://graph.facebook.com/' + event.fb_post_id + '/comments?%s' % params).read()
    )

    for question in questions['data']:
        new_question = {
            'fb_id':    question['id'],
            'user':     question['from']['id'],
            'question': question['message'],
            'event_id': event.id
        }

        db_q = db.session.query(Question).filter(
            Question.fb_id == question['id']
        ).first()

        if not db_q:
            groups = db.session.query(Group).filter(
                Group.event_id == event.id
            ).all()

            g = None
            if groups:
                g = match_group(new_question['question'], groups, 0.9)

            if g is None:
                g = {
                    'event_id': event.id,
                    'question': new_question['question']
                }

                # Get Sentiment
                params = {
                    'apikey':     '2ccd6f653c1e4253b6ac5ee0dadb284bde58331e',
                    'text':       new_question['question'],
                    'outputMode': 'json'
                }
                params = urllib.urlencode(params)

                sentiment = json.loads(
                    urllib.urlopen('http://access.alchemyapi.com/calls/text/TextGetTextSentiment?%s' % params).read()
                )

                if 'docSentiment' in sentiment and 'type' in sentiment['docSentiment']:
                    if sentiment['docSentiment']['type']:
                        g['sentiment'] = sentiment['docSentiment']['type']

                g = Group(**g)

                db.session.add(g)
                db.session.commit()

            new_question['group_id'] = g.id

            q = Question(**new_question)

            db.session.add(q)
            db.session.commit()

    return Response(json.dumps({
        'status': questions
    }), mimetype='application/json')


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


@app.route('/dashboard/event/<event_id>/polling')
def dashboard_polling(event_id):
    event = db.session.query(Event).filter(
        Event.id == event_id
    ).first()

    page = db.session.query(Page).filter(
        Page.id == event.page_id
    ).first()

    aGroups = db.session.query(Group).filter(
        Group.event_id == event_id
    ).filter(
        Group.status == 1
    ).all()

    uGroups = db.session.query(Group).filter(
        Group.event_id == event_id
    ).filter(
        Group.status == 0
    ).all()

    questions = db.session.query(Question).filter(
        Question.event_id == event.id
    ).count()

    return Response(json.dumps({
        'questionsNumber': questions,
        'usersOverview': 100,
        'answeredQuestions': [i.serialize for i in aGroups],
        'unansweredQuestions': [i.serialize for i in uGroups]
    }), mimetype='application/json')


@app.route('/dashboard/event/<event_id>/publish')
def dashboard_publish(event_id):
    event = db.session.query(Event).filter(
        Event.id == event_id
    ).first()

    page = db.session.query(Page).filter(
        Page.id == event.page_id
    ).first()

    params = {
        'access_token':       page.token,
        'to':                 page.page_id,
        'message':            'This is an awesome post. Deal with it!',
        'format':             'json',
        'suppress_http_code': 1,
        'method':             'post'
    }
    params = urllib.urlencode(params)

    data = json.loads(
        urllib.urlopen('https://graph.facebook.com/' + page.page_id + '/feed?%s' % params).read()
    )

    if 'id' in data:
        event.fb_post_id = data['id']
        event.status = 1
        db.session.commit()

    return redirect('/dashboard/page/%s' % page.page_id)


@app.route('/dashboard/new', methods=['POST'])
def dashboard_new():
    form = request.form

    page_id = form['session-page']

    page = db.session.query(Page).filter(
        Page.page_id == page_id
    ).first()

    new_event = {
        'page_id': page.id,
        'title': form['session-title'],
        'message': 'This is a random message'
    }

    if form['session-start-date']:
        new_event['start_date'] = datetime.datetime.strptime(form['session-start-date'], '%Y/%m/%d %H:%M')

    if form['session-end-date']:
        new_event['end_date'] = datetime.datetime.strptime(form['session-end-date'], '%Y/%m/%d %H:%M')

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
    else:
        db_page.token = access_token

    db.session.commit()

    return redirect('/dashboard/page/%s' % page_id)
