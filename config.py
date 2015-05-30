from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
# debug mode is enable or disable
app.debug = True
app.secret_key = 'aQRaFWWWaAa!#$43$aa!!!AsSSQ'

# import os
# create database connection for sqlite3
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "sample.db")
# app.database = db_path

# create connection for sqlachemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'

# connect with mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskdb'

# create sqlalchemy object
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
