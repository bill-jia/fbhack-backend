"""
models.py

Define models relating to the project, for examples users,
or the tastes shared by users.
"""
from datetime import datetime
from flask.ext.login import UserMixin

from app import db

artist_preference_association_table = db.Table(
    'artist_preference_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
    db.PrimaryKeyConstraint('user_id', 'artist_id')
)

song_preference_association_table = db.Table(
    'song_preference_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id')),
    db.PrimaryKeyConstraint('user_id', 'song_id')
)

group_membership_association_table = db.Table(
    'group_memberships',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.PrimaryKeyConstraint('user_id', 'group_id')
)

class User(UserMixin, db.Model):
    """
    Define a user, and associated information. This will primarily be things
    like Spotify ID and email address.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)

    # This can be used for querying the Spotify API
    spotify_id = db.Column(db.String(64), nullable=False, unique=True)

    preferences_last_updated = db.Column(db.DateTime(), nullable=False, default=datetime.today)

    # Artists that this user likes
    artist_preferences = db.relationship("Artist", secondary=artist_preference_association_table, backref='users', lazy='dynamic')
    song_preferences = db.relationship("Song", secondary=song_preference_association_table, backref='users', lazy='dynamic')


class Group(db.Model):
    """
    Define a group, as a many-to-many mapping between users and other users.

    In order to join the group, we'll probably have a url that people can either
    navigate to using a QR code, or get to by just entering a code into their browser.

    I don't think it needs to be thaaat secure, so we can probably just use the group
    name as a key in that case - if we decide that it should be harder to guess the
    url, we could use a random string (preferably human readable).
    """
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)

    # We can allow the user to create this themselves
    name = db.Column(db.String(64), nullable=False)

    # The user that initially creates the group can be known as the 'host'
    host = db.Column(db.Integer, db.ForeignKey('users.id'))

    members = db.relationship("User", secondary=group_membership_association_table, backref='groups')


class Artist(db.Model):
    """
    Define an artist as a shared interest between two users. You can think of
    this as an edge on a graph, in which users are vertices. It would probably
    make sense to use a graph database for this at some point, however we can get
    away with using a relational database for the time being.
    """
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)

    # Store the spotify id of the artist that they have in common
    spotify_id = db.Column(db.String(64), nullable=False, unique=True)


class Song(db.Model):
    """
    Define a song as a shared interest between two users. Analogous to the artist
    preference above. At some point, this should probably be refactored to be
    represented by the same model as the artist one.
    """
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)

    # Store the spotify id of the song that they have in common
    spotify_id = db.Column(db.String(64), nullable=False, unique=True)

