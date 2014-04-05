from api.core import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    created = db.Column(db.DateTime)

    def __init__(self, *args, **kwargs):
        for key in kwargs:
          setattr(self, key, kwargs[key])

    @property
    def serialize(self):
        return {
            'fb_id': self.fb_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
