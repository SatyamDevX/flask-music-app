from flask import Blueprint, render_template, request, current_app, redirect, flash, url_for

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user, login_required

import os


from music.models import db, Song, PlaylistSong, Playlist, Role, User
from sqlalchemy.orm import joinedload


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/playlists')
@login_required
def user_dashboard():
   songs = Song.query.all()
    # Load playlists for user ID 2, including songs inside them
   playlists_user_2 = Playlist.query.options(joinedload(Playlist.songs).joinedload(PlaylistSong.song))\
                                    .filter_by(user_id=current_user.id).all()

   return render_template('user_playlists.html', songs=songs, playlists_user_2=playlists_user_2)

@user_bp.route('/creator_register')
@login_required
def creator_registration():
    if current_user.is_creator:
        flash('You are already a creator.', 'info')
    elif current_user.creator_requested:
        flash('You have already requested creator access. Please wait for admin approval.', 'info')
    else:
        current_user.creator_requested = True
        db.session.commit()
        flash('Your request to become a creator has been submitted for admin approval.', 'success')

    return redirect(request.referrer)

@user_bp.route('/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    # user = User.query.get(2)
    # user.username = 'Satyam Srivastava'
    # db.session.commit()
    return render_template('user_profile.html', user=user)




