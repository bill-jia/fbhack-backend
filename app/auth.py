import sys
import spotipy
import spotipy.util as util

from flask import redirect, url_for
from flask.ext.login import LoginManager, current_user
from app import app, lm, db

from .models import User

scope = 'user-library-read user-follow-read user-read-email'

@lm.user_loader
def load_user(_id):
	return User.query.get(int(_id))

@app.route('/')
@app.route('/index')
def index():
	return "Hello World!"

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
			print(user)
			# If the user does not exist on our database, register them
			if User.query.filter_by(spotify_id=user['id']).first() == None:
				newUser = User(name=user['display_name'], spotify_id=user['id'], email=user['email'])
				db.session.add(newUser)
				db.session.commit()
				print("new user registered!")
			else:
				print("user already exists")
			#update data in our database
			#updateSpotifyData(sp)

		else:
			print("authentication failed!")
	return redirect(url_for('index'))
