from flask import Flask
from flask import session
from flask import Response
from flask import request
from flask import redirect, url_for
from flask import render_template

from api.core import app, db
from api.models.user import User
from api.models.page import Page
from gensim import corpora, models, similarities

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

def match_similar(inputs, questions):
    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in question.lower().replace('?', '').split() if word not in stoplist] for question in questions]

    # Create dictionary
    dictionary = corpora.Dictionary(texts)

    # Define corpus
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Define LSI space
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    # Get similarity of teh doc vs documents
    vector = dictionary.doc2bow(inputs.lower().split())
    vector_lsi = lsi[vector]

    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vector_lsi]

    return sims

def match_group(inputs, groups, min_threshold):
    group_questions = []
    for group in groups:
        group_questions.append(group.question)

    group_similarity = sorted(enumerate(match_similar(inputs, group_questions)), key=lambda item: -item[1])

    for group_id, similarity in group_similarity:
        if similarity > min_threshold:
            return groups[group_id]

    # Create new group
    return None
