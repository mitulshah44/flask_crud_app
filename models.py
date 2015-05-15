from config import db

class User(db.Model):

    __tablename__ = 'userdata'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '{} {}'.format(self.username, self.email)
