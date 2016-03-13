import random

from flask import abort, Response
from flask.ext.login import current_user

from app import app
from .models import User, Group

@app.route('/group/<groupid>/playlist/')
@app.route('/group/<groupid>/playlist/<length>')
def generate_playlist(groupid, length=10):
    # firstly, make sure that the user is authenticated
    if current_user.is_anonymous:
        # Unauthorised!
        abort(403)

    # make sure that the user is in the group
    if Group.query.get(groupid) not in current_user.groups:
        abort(403)

    # Get the current user from the database
    print(current_user.spotify_id)

    # Perform a random walk of the 'songs' graph, chosing a random edge
    # at each point. In the future, it would be nice to do something more
    # advanced, like trying to make sure that there is an even representation
    # of each person's musical tastes.

    # This is probably going to use an annoyingly large number of database
    # operations, but that should be ok for the time being.

    songs = set()
    user = current_user

    while len(songs) < length:
        likes = user.song_preferences.all()

        if len(likes) == 0:
            # TODO: implement this case
            break

        song = likes[random.randrange(len(likes))]

        if song.spotify_id not in songs:
            songs.add(song.spotify_id)
        else:
            likes.remove(song)
            while len(likes) > 0:
                song = likes[random.randrange(len(likes))]

                if song.spotify_id not in songs:
                    songs.add(song.spotify_id)
                    break
                else:
                    likes.remove(song)
            break
        print(song.users)
        linked_users = [user for user in song.users if User.groups.any(id=groupid) is not None]

        # pick a random user (preferably not this one)
        if len(linked_users) > 1:
            # there's a user other than this one
            linked_users.remove(user)
            user = random.choice(linked_users)

    return Response("")
