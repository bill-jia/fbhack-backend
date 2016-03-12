import os
import sys
import spotipy
from spotipy import util, oauth2

from flask import redirect, url_for, abort, request
from flask.ext.login import LoginManager, current_user, login_user, logout_user
from app import app, lm, db

from .models import User, Group
from .helpers import updateSpotifyData

scope = 'user-library-read user-follow-read user-read-email'

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

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

@app.route('/authorize/')
def auth():
	auth_url = sp_oauth.get_authorize_url()
	print(auth_url)

	return redirect(auth_url)

@app.route('/authorized/')
def authorized():
	"""
	Requests OAuth from Spotify and signs up new users onto database. Updates users' lists of
	songs, playlists, artists.
	"""

	code = sp_oauth.parse_response_code(request.url)
	token_info = sp_oauth.get_access_token(code)

	token = token_info['access_token']

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
