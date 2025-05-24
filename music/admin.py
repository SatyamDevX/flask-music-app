from flask import Blueprint, render_template, request, current_app, redirect

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user, login_required

import os


from music.models import db, Song, PlaylistSong, Playlist, Album
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route('/dashboard')
@login_required
def admind_ashboard():
   songs = Song.query.all()
   albums = Album.query.all()

   return render_template("admin_dashboard.html", albums=albums, songs=songs)