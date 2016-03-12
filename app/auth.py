import sys
import spotipy
import spotipy.util as util

from flask import redirect, url_for
from flask.ext.login import LoginManager, current_user
from app import app, lm

from .models import User

scope = 'user-library-read user-follow-read'

@lm.user_loader
def load_user(_id):
	return User.query.get(int(_id))

@app.route('/')
@app.route('/index')
def index():
	return "Hello World!"

@app.route('/authorize/<username>')
def authorize(username):
	if current_user.is_anonymous:
		token = util.prompt_for_user_token(username, scope)
		if token:
			sp = spotipy.Spotify(auth=token)
			artists = sp.current_user_followed_artists()
			tracks = sp.current_user_saved_tracks()
			playlists = sp.user_playlists(username)
			print(artists)
		else:
			print("authentication failed!")
	return redirect(url_for('index'))
