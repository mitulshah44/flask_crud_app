from config import db, manager


class User(db.Model):

    __tablename__ = 'userdata'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(250))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '{} {}'.format(self.username, self.email)


class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    # userid = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('userdata.id'))
    bookname = db.Column(db.String(50))

    def __init__(self, userid, bookname):
        self.userid = userid
        self.bookname = bookname

    def __repr__(self):
        return '{} {}'.format(self.userid, self.bookname)

if __name__ == '__main__':
    manager.run()
