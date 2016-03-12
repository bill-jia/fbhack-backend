"""
Setup useful Flask objects: app, database and login manager.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

import binascii
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = binascii.hexlify(os.urandom(24))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spotty.db'

db = SQLAlchemy(app)
lm = LoginManager(app)

from . import auth, models, generate
