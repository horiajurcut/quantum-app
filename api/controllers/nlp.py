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
import pprint

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

@app.route('/nlp/similar')
def nlp_similar():
    documents = [
        "This is not good at all",
        "Human machine interface for lab abc computer applications",
        # "A survey of user opinion of computer system response time",
        # "The EPS user interface management system",
        # "System and human system engineering testing of EPS",
        # "Relation of user perceived response time to error measurement",
        # "The generation of random binary unordered trees",
        # "The intersection graph of paths in trees",
        # "Graph minors IV Widths of trees and well quasi ordering",
        "Graph minors A survey"]

    # remove common words and tokenize
    stoplist = set('for a of the and to in by from on with as a '.split())
    texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]

    # Create dictionary
    dictionary = corpora.Dictionary(texts)

    # Define corpus
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Define LSI space
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=10)

    # Get similarity of teh doc vs documents
    doc = "Human computer interaction"
    vector = dictionary.doc2bow(doc.lower().split())
    vector_lsi = lsi[vector]

    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vector_lsi]

    return Response(json.dumps(sims), mimetype='application/json')