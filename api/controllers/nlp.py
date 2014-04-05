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


@app.route('/nlp/sentiment')
def nlp_sentiment():
    params = {
        'apikey':     '2ccd6f653c1e4253b6ac5ee0dadb284bde58331e',
        'text':       'I hate this tv show. It became really booring.',
        'outputMode': 'json'
    }
    params = urllib.urlencode(params)

    sentiment = json.loads(
        urllib.urlopen('http://access.alchemyapi.com/calls/text/TextGetTextSentiment?%s' % params).read()
    )

    return Response(json.dumps({
        'accounts': sentiment
    }), mimetype='application/json')


@app.route('/nlp/rank_keywords')
def npl_rank_keywords():
    params = {
        'apikey':     '2ccd6f653c1e4253b6ac5ee0dadb284bde58331e',
        'text':       'I hate this tv show. It became really booring.',
        'outputMode': 'json',
        'sentiment':  1
    }
    params = urllib.urlencode(params)

    ranked = json.loads(
        urllib.urlopen('http://access.alchemyapi.com/calls/text/TextGetRankedKeywords?%s' % params).read()
    )

    return Response(json.dumps({
        'accounts': ranked
    }), mimetype='application/json')
