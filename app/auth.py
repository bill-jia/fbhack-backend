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
			updateSpotifyData(sp)

		else:
			print("authentication failed!")
	return redirect(url_for('index'))

def updateSpotifyData(spotify):
	"""
	Update songs, playlists, artists upon login
	"""
	lim = 50
	artists = spotify.current_user_followed_artists(limit=lim)
	totalArtists = artists["artists"]["total"]
	if totalArtists > lim:
		pages = int((totalArtists-(lim+1))/lim)+1
		for i in range(1,pages):
			nextCursor = artists["artists"]["cursors"]["after"]
			artists = spotify.current_user_followed_artists(limit=lim, after=nextCursor)
	
	tracks = spotify.current_user_saved_tracks(limit=lim)
	totalTracks = tracks["total"]
	# for track in tracks["items"]:
	# 	print(track["track"]["name"])
	if totalTracks > lim:
		pages = int((totalTracks-(lim+1))/lim)+1
		for i in range(1,pages):
			tracks = spotify.current_user_saved_tracks(limit=lim, offset=i*lim)
			# for track in tracks["items"]:
			# 	print(track["track"]["name"].encode('utf-8'))			

	userId = spotify.current_user()["id"]
	playlists = spotify.user_playlists(userId, limit=lim)
	totalPlaylists = playlists["total"]
	getTracksFromPlaylists(playlists, spotify)
	if totalPlaylists > lim:
		pages = int((totalPlaylists-(lim+1))/lim)+1
		for i in range(1,pages):
			playlists = spotify.user_playlists(userId, limit=lim, offset=i*lim)
			getTracksFromPlaylists(playlists, spotify)

def getTracksFromPlaylists(playlists, spotify):
	"""
	Get all the songs off a group fo playlists
	"""
	lim = 100
	for playlist in playlists["items"]:
		if playlist["public"]:
			playlistId = playlist["id"]
			userId = playlist["owner"]["id"]
			tracks = spotify.user_playlist_tracks(userId, playlistId, limit=lim)
			totalTracks = tracks["total"]
			if totalTracks > lim:
				pages = int((totalTracks-(lim+1))/lim)+1
				for i in range(1,pages):
					tracks = spotify.user_playlist_tracks(userId, playlistId, limit=lim, offset=i*lim)