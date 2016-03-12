"""
Setup useful Flask objects: app, database and login manager.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

app = Flask(__name__)

# TODO, change this in production
app.config['SECRET_KEY'] = "65206bed256e7f1bdb0e87574136f3e9a6e3b4848a71a355"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotty.db'

db = SQLAlchemy(app)
lm = LoginManager(app)

from . import auth, models, generate, views
