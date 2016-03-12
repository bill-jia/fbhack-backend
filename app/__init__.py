from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)
lm = LoginManager(app)


from app import auth

