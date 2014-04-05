from api.core import db


class Page(db.Model):
    __tablename__ = 'pages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    page_id = db.Column(db.String(100))
    token = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        for key in kwargs:
          setattr(self, key, kwargs[key])

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'page_id': self.page_id,
            'token': self.token
        }
