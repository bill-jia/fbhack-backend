"""
models.py

Define models relating to the project, for examples users,
or the tastes shared by users.
"""

from flask.ext.login import UserMixin

from app import db


class User(UserMixin, db.Model):
    """
    Define a user, and associated information. This will primarily be things
    like Spotify ID and email address.
    """
    __tablename__ = 'users'

    _id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    # This can be used for querying the Spotify API
    spotify_id = db.Column(db.String(64), nullable=False, unique=True)


class ArtistPreference(db.Model):
    """
    Define an artist as a shared interest between two users. You can think of
    this as an edge on a graph, in which users are vertices. It would probably
    make sense to use a graph database for this at some point, however we can get
    away with using a relational database for the time being.
    """
    __tablename__ = 'artist_preferences'

    _id = db.Column(db.Integer, primary_key=True)
