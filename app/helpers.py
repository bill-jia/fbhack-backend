from .models import User, Artist, Song
from app import db
from datetime import datetime
import dateutil.parser
from sqlalchemy.exc import IntegrityError


def updateSpotifyData(spotify, user):
	"""
	Update songs, playlists, artists upon login
	"""
	lim = 50
	artists = spotify.current_user_followed_artists(limit=lim)


	for artist in artists["artists"]["items"]:
		tryAddArtist(user, artist)

	totalArtists = artists["artists"]["total"]
	if totalArtists > lim:
		pages = int((totalArtists-(lim+1))/lim)+1
		for i in range(pages):
			nextCursor = artists["artists"]["cursors"]["after"]
			artists = spotify.current_user_followed_artists(limit=lim, after=nextCursor)
			for artist in artists["artists"]["items"]:
				tryAddArtist(user, artist)		

	tracks = spotify.current_user_saved_tracks(limit=lim)
	totalTracks = tracks["total"]
	contFlag = True
	for track in tracks["items"]:
		if user.preferences_last_updated < dateutil.parser.parse(track["added_at"], ignoretz=True):
			tryAddTrack(user, track)
			print("track added")
		else:
			contFlag= False
			break

	if totalTracks > lim and contFlag:
		pages = int((totalTracks-(lim+1))/lim)+1
		for i in range(pages):
			tracks = spotify.current_user_saved_tracks(limit=lim, offset=(i+1)*lim)
			for track in tracks["items"]:
				if user.preferences_last_updated < dateutil.parser.parse(track["added_at"], ignoretz=True):
					tryAddTrack(user, track)
					# print("track added")
				else:
					contFlag= False
					break
			if not contFlag:
				break

	userId = spotify.current_user()["id"]
	playlists = spotify.user_playlists(userId, limit=lim)
	totalPlaylists = playlists["total"]
	getTracksFromPlaylists(playlists, spotify, user)
	if totalPlaylists > lim:
		pages = int((totalPlaylists-(lim+1))/lim)+1
		for i in range(pages):
			playlists = spotify.user_playlists(userId, limit=lim, offset=(i+1)*lim)
			getTracksFromPlaylists(playlists, spotify)
	
	user.preferences_last_updated = datetime.today()
	db.session.commit()

def getTracksFromPlaylists(playlists, spotify, user):
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
			pages = int(totalTracks/lim)+1
			contFlag = False
			for i in range(pages, 0, -1):
				tracks = spotify.user_playlist_tracks(userId, playlistId, limit=lim, offset=(i-1)*lim)
				for track in reversed(tracks["items"]):
					if user.preferences_last_updated < dateutil.parser.parse(track["added_at"], ignoretz=True):
						tryAddTrack(user, track)
						print("track added")
					else:
						contFlag= False
						break
				if not contFlag:
					break

def tryAddTrack(user, track):
	# ignore tracks that aren't on spotify
	if 'is_local' in track and track['is_local']:
		return

	if not user.song_preferences.filter_by(spotify_id=track["track"]["id"]).first():
		newSong = Song(spotify_id=track["track"]["id"], preview_url=track["track"]["preview_url"])
		try:
			db.session.add(newSong)
			db.session.flush()
		except IntegrityError:
			pass
		song = Song.query.filter_by(spotify_id=track["track"]["id"]).one()
		user.song_preferences.append(song)

def tryAddArtist(user, artist):
	if not user.artist_preferences.filter_by(spotify_id=artist["id"]).first():
		newArtist = Artist(spotify_id=artist["id"])
		try:
			db.session.add(newArtist)
			db.session.flush()
		except IntegrityError:
			pass
		artist = Artist.query.filter_by(spotify_id=artist["id"]).one()
		user.artist_preferences.append(artist)