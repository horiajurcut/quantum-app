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
    texts = [[word for word in question.lower().split() if word not in stoplist] for question in questions]

     # remove words that appear only once
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once] for text in texts]

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
    for key, group in groups.items():
        group_questions.append(group['content'])
    
    group_similarity = sorted(enumerate(match_similar(inputs, group_questions)), key=lambda item: -item[1])

    for group_id, similarity in group_similarity:
        if similarity > min_threshold:
            return groups[str(group_id)]

    # Create new group
    print('New Group created');
    

@app.route('/nlp/similar')
def nlp_similar():
    min_threshold = 0.4;

    groups = {
        '1': {
            'id': 1,
            'content': 'The EPS user interface management system'
        },
        '2': {
            'id': 2,
            'content': 'Human machine interface for lab abc computer applications'
        },
        '3': {
            'id': 3,
            'content': 'System and human system engineering testing of EPS'
        },
        '4': {
            'id': 4,
            'content': 'A survey of user opinion of computer system response time'
        }
    }

    questions = { 
        '1': {
            'id': 1,
            'question': "Human machine interface for lab abc computer applications",
            'similarity': 0.9,
            'group_id': 1
        },
        '2': {
            'id': 2,
            'question': "A survey of user opinion of computer system response time",
            'similarity': 9.1,
            'group_id': 1
        },
        '3': {
            'id': 3,
            'question': "The EPS user interface management system",
            'similarity': 0.6,
            'group_id': 2
        },
        '4': {
            'id': 4,
            'question': "System and human system engineering testing of EPS",
            'similarity': 7.7,
            'group_id': 2
        },
        '5': {
            'id': 5,
            'question': "Relation of user perceived response time to error measurement",
            'similarity': 8.1,
            'group_id': 0
        },
        '6': {
            'id': 6,
            'question': "The generation of random binary unordered trees",
            'similarity': 7.2,
            'group_id': 1
        },
        '7': {
            'id': 7,
            'question': "The intersection graph of paths in trees",
            'similarity': 1.6,
            'group_id': 2
        },
        '8': {
            'id': 8,
            'question': "Graph minors IV Widths of trees and well quasi ordering",
            'similarity': 2.3,
            'group_id': 0
        },
        '9': {
            'id': 6,
            'question': "Graph minors A survey",
            'similarity': 3.1,
            'group_id': 1
        }
    }

    inputs = "Human computer interaction"
    sims = match_group(inputs, groups, min_threshold)

    return Response(json.dumps(sims), mimetype='application/json')
