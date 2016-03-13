"""
Setup useful Flask objects: app, database and login manager.
"""

import json

from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

app = Flask(__name__)

# TODO, change this in production
app.config['SECRET_KEY'] = "65206bed256e7f1bdb0e87574136f3e9a6e3b4848a71a355"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotty.db'

db = SQLAlchemy(app)

class UserJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, db.Model):
            return o._asdict()
        else:
            return super.default(o)
app.json_encoder = UserJSONEncoder

lm = LoginManager(app)

from . import auth, models, generate, views
