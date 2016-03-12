import sys
import spotipy
import spotipy.util as util

from flask import redirect, url_for, abort
from flask.ext.login import LoginManager, current_user, login_user, logout_user
from app import app, lm, db

from .models import User, Group
from .helpers import updateSpotifyData

scope = 'user-library-read user-follow-read user-read-email'

@lm.user_loader
def load_user(_id):
	return User.query.get(int(_id))

@app.route('/')
@app.route('/index')
def index():
	if current_user.is_anonymous:
		return "Hello World"
	return '<a href="/logout">Log Out</a>'

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/authorize/<username>')
def authorize(username):
	"""
	Requests OAuth from Spotify and signs up new users onto database. Updates users' lists of
	songs, playlists, artists.
	"""
	if current_user.is_anonymous:
		token = util.prompt_for_user_token(username, scope)
		if token:
			sp = spotipy.Spotify(auth=token)
			user = sp.current_user()

			# If the user does not exist on our database, register them
			user_object = User.query.filter_by(spotify_id=user['id']).first()

			if user_object is None:
				newUser = User(name=user['display_name'] or user['id'], spotify_id=user['id'], email=user['email'])
				db.session.add(newUser)
				db.session.commit()
				login_user(newUser)
				user_object = User.query.filter_by(spotify_id=user['id']).first()
				print("new user registered!")
			else:
				val = login_user(user_object)
				print("user already exists")
				print(val)

			# update data in our database
			updateSpotifyData(sp, user_object)

		else:
			print("authentication failed!")

	return redirect(url_for('index'))
