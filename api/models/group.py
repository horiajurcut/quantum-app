from api.core import db
from api.models.question import Question

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
        q = db.session.query(Question).filter(
            Question.group_id = self.id
        ).count()

        return {
            'id': self.id,
            'question': self.question,
            'sentiment': self.sentiment,
            'frequency': q
        }
