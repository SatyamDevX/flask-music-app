from flask import Blueprint, render_template, request, current_app, redirect

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user

import os


from music.models import db, Song, PlaylistSong, Playlist
from sqlalchemy.orm import joinedload


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
def userdashboard():
   songs = Song.query.all()
    # Load playlists for user ID 2, including songs inside them
   playlists_user_2 = Playlist.query.options(joinedload(Playlist.songs).joinedload(PlaylistSong.song))\
                                    .filter_by(user_id=2).all()

   return render_template('user_dashboard.html', songs=songs, playlists_user_2=playlists_user_2)


