from api.core import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String(100), unique=True)
    question = db.Column(db.String(2000))
    group_id = db.Column(db.Integer, nullable=True)

    def __init__(self, *args, **kwargs):
        for key in kwargs:
          setattr(self, key, kwargs[key])

    @property
    def serialize(self):
        return {
            'fb_id': self.fb_id,
            'question': self.question
        }
