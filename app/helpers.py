from .models import User, Artist, Song

def updateSpotifyData(spotify, user):
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
	getTracksFromPlaylists(playlists, spotify, user)
	if totalPlaylists > lim:
		pages = int((totalPlaylists-(lim+1))/lim)+1
		for i in range(1,pages):
			playlists = spotify.user_playlists(userId, limit=lim, offset=i*lim)
			getTracksFromPlaylists(playlists, spotify)

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
			if totalTracks > lim:
				pages = int((totalTracks-(lim+1))/lim)+1
				for i in range(1,pages):
					tracks = spotify.user_playlist_tracks(userId, playlistId, limit=lim, offset=i*lim)
