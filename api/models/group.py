from api.core import db


class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    question = db.Column(db.String(2000))

    def __init__(self, *args, **kwargs):
        for key in kwargs:
          setattr(self, key, kwargs[key])

    @property
    def serialize(self):
        return {
            'question': self.question
        }
