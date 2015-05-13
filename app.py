# import python module
from json import *
from functools import wraps
import sqlite3
import os

# import flask module
from flask import (Flask, views, render_template,
                   request, flash, redirect, url_for, session,
                   g)
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# import project modules
from models import *

app = Flask(__name__)

# debug mode is enable or disable
app.debug = True
app.secret_key = 'aQRaFWWWaAa!#$43$aa!!!AsSSQ'

# create database connection for sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "sample.db")
app.database = db_path

# create connection for sqlachemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'

# connect with mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskdb'

# create sqlalchemy object
db = SQLAlchemy(app)

data = {}


class Viewpage(views.MethodView):
    """
    """
    def get(self):
        data['title'] = "Subscription"
        # g.db = connect_db()
        # cur = g.db.execute('select * from userdata')
        # usrdata = [dict(username=row[0], email=row[1])
        #            for row in cur.fetchall()]
        # g.db.close()
        usrdata = db.session.query(User).all()

        return render_template('index.html', data=data, userdata=usrdata)

    def post(self):
        data['title'] = "Subscription"
        data['message'] = "POST Method is called."
        data['content'] = email = request.form['expression']
        uname = session['username']

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

        # fetch data from userdata table
        usrdata = db.session.query(User).all()

        return render_template('index.html', data=data, userdata=usrdata)

app.add_url_rule('/', view_func=Viewpage.as_view('main'),
                 methods=['GET', 'POST'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return decorated_function


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
        uname = request.form['username']
        udata = User.query.filter(User.username == uname,
                                  User.email == email).all()
        print udata, User

        if len(udata) > 0:
            for u in udata:
                session['logged_in'] = True
                session['id'] = u.id
                session['username'] = request.form['username']
                session['email'] = request.form['email']
                return redirect(url_for('homepage'))
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error, data=data)


# @app.route('/user/', defaults={'userid': 1})
@app.route('/user/<int:userid>')
def show_user(userid):
    pass
    # user = User.query.filter_by(userid=userid).first_or_404()
    # return render_template('show_user.html', user=user)


@app.route("/delete/user/<int:userid>")
def deleteUser(userid):
    # u = User.query.filter(id == userid).all().delete()
    # u = User.query.filter(User.id == userid).first()
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
    # session.pop('logged_in', None)
    # session.pop('username', None)
    # session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/')
@login_required
def homepage():
    data['title'] = 'Subscription'
    g.db = connect_db()
    cur = g.db.execute('select * from userdata')
    usrdata = [dict(username=row[0], email=row[1]) for row in cur.fetchall()]
    g.db.close()

    return render_template('index.html', data=data, userdata=usrdata)


# connection with sqlite3
def connect_db():
    return sqlite3.connect(app.database)

if __name__ == "__main__":
    app.run()

# execute raw query like db.engine.execute("delete from users where id=...")
