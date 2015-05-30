# import python module
from json import *
from functools import wraps
import sqlite3

# import flask module
from flask import (views, render_template,
                   request, flash, redirect, url_for, session,
                   g)
from werkzeug.security import generate_password_hash, \
                check_password_hash

from sqlalchemy.exc import IntegrityError

# import project modules
from config import db, app
from models import *

data = {}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return decorated_function


def set_password(password):
    return generate_password_hash(password)


def check_password(password):
    return check_password_hash(self.pw_hash, password)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    data['title'] = 'Login Page'
    if request.method == 'POST':
        # g.db = connect_db()
        # cur = g.db.execute('select * from userdata where email="{}"'.format(
        #     request.form['email']))
        # usrdata = [dict(username=row[0], email=row[1])
        #            for row in cur.fetchall()]
        # g.db.close()
        email = request.form['email']
        password = request.form['password']

        udata = User.query.filter(User.password == password,
                                  User.email == email).all()
        if len(udata) > 0:
            for u in udata:
                session['logged_in'] = True
                session['id'] = u.id
                session['username'] = u.username
                session['email'] = u.email
                return redirect(url_for('homepage'))
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error, data=data)


# @app.route('/user/', defaults={'userid': 1})
@app.route('/user/<int:userid>')
def show_user(userid):
    """
    to view user information
    """
    data['title'] = 'Edit User'
    user = User.query.filter_by(id=userid).first_or_404()
    # user = User.query.all()
    jsondata = {'id': user.id, 'username': user.username,
                'email': user.email}
    print jsondata
    return render_template('show_user.html', user=jsondata, data=data)


@app.route('/updateinfo', methods=['POST'])
def updateInfo():
    """
    to update information
    """
    email = request.form['email']
    uname = request.form['username']
    uid = request.form['id']
    User.query.filter_by(id=uid).update(dict(email=email,
                                             username=uname))
    db.session.commit()
    return redirect(url_for('homepage'))


@app.route("/delete/user/<int:userid>")
def deleteUser(userid):
    """
    Used function to delete user permanently
    """
    user = User.query.get(userid)
    db.session.remove()
    db.session.delete(user)
    db.session.commit()

    # User.query.filter_by(id=userid).delete()
    # s = session
    # u = s.query(User).filter(User.id == userid).one()
    # s.delete(u)
    # s.commit()
    # db.session.delete(u)
    # db.session.commit()
    return redirect(url_for('homepage'))


@app.route('/logout')
def logout():

    session.clear()
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def homepage():
    data['title'] = 'Add Book'
    # fetch data usinf raw query
    # g.db = connect_db()
    # cur = g.db.execute('select * from userdata')
    # usrdata = [dict(username=row[0], email=row[1]) for row in cur.fetchall()]
    # g.db.close()

    # fetching data using sqlachemy
    # usrdata = User.query.all()
    # sample join userList = users.query.join(friendships, users.id==friendships.user_id).add_columns(users.userId, users.name, users.email, friends.userId, friendId).filter(users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
    Booklist = Book.query.join(User).filter(User.id==Book.userid).all()
    print Booklist
    return render_template('index.html', data=data, bookdata=Booklist)


@app.route('/addbook', methods=['POST'])
@login_required
def addBook():
    """
    Add favorite book of user
    """
    book = request.form['book']
    email = session['email']
    user = User.query.filter_by(email=email).first_or_404()
    try:
        db.session.add(Book(user.id, book))
        db.session.commit()
        message = book + " has been added in your account."
        flash(message)
    except IntegrityError as e:
        db.session.rollback()
        flash(str(e.message))
        pass
    return redirect(url_for('homepage'))


class Indexpage(views.MethodView):
    """
    Viewpage class is easy to access where
    we can defind get post put method
    using class method
    """
    def get(self):
        data['title'] = "List of Member"
        # g.db = connect_db()
        # cur = g.db.execute('select * from userdata')
        # usrdata = [dict(username=row[0], email=row[1])
        #            for row in cur.fetchall()]
        # g.db.close()
        usrdata = db.session.query(User).all()
        print usrdata
        return render_template('member.html', data=data, userdata=usrdata)

app.add_url_rule('/member', view_func=Indexpage.as_view('main'),
                 methods=['GET', 'POST'])


class AddMember(views.MethodView):
    """
    Add new member using post method
    url /AddMember
    """
    def post(self):
        data['title'] = "Subscription"
        data['message'] = "POST Method is called."
        data['content'] = email = request.form['email']
        uname = request.form['username']

        # insert email into database
        try:
            db.session.add(User(uname, email))
            db.session.commit()
            message = data['content'] + " has been added."
            flash(message)
        except IntegrityError as e:
            db.session.rollback()
            flash(str(e.message))
            pass

        return redirect(url_for('main'))

app.add_url_rule('/AddMember', view_func=AddMember.as_view('addmember'),
                 methods=['POST'])


# connection with sqlite3
def connect_db():
    return sqlite3.connect(app.database)

if __name__ == "__main__":
    app.run()

# execute raw query like db.engine.execute("delete from users where id=...")
