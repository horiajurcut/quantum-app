from api.core import db

import random


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    question = db.Column(db.String(2000))
    sentiment = db.Column(db.String(30), nullable=True)
    status = db.Column(db.Integer, default=0)
    answer = db.Column(db.String(2000), nullable=True)

    def __init__(self, *args, **kwargs):
        for key in kwargs:
          setattr(self, key, kwargs[key])

    @property
    def serialize(self):
        return {
            'id': self.id,
            'question': self.question,
            'sentiment': self.sentiment,
            'frequency': random.randint(100, 1000)
        }
