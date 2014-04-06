from api.core import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    fb_post_id = db.Column(db.String(255), nullable=True)
    page_id = db.Column(db.Integer)
    title = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    message = db.Column(db.String(1000))
    status = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        for key in kwargs:
          setattr(self, key, kwargs[key])

    @property
    def serialize(self):
        return {
            'title': self.title,
            'message': self.message
        }
