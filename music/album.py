from flask import Blueprint, render_template, request, current_app, redirect, url_for, jsonify

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user, login_required

import os


from music.models import db, Song, Playlist, PlaylistSong, Album


album_bp = Blueprint('album', __name__, url_prefix='/album')

@album_bp.route('/create', methods=['POST'])
@login_required
def create_album():
   title = request.form['title']
   if not title:
    return jsonify({'error': 'Title is required'}), 400

   new_album = Album(title=title, creator_id=current_user.id)
   db.session.add(new_album)
   db.session.commit()

   # return jsonify({'message': 'Album created', 'album_id': new_album.id}), 201
   return redirect(request.referrer)



@album_bp.route('/', methods=['GET'])
def view_albums():
   albums = Album.query.all()
   # album_list = []
   # for album in albums:
   #    album_list.append({
   #    'id': album.id,
   #    'title': album.title,
   #    'creator': album.creator.username if album.creator else None,
   #    'songs': [{'id': s.id, 'title': s.title} for s in album.songs]
   #    })
   return render_template("admin_dashboard.html", albums=albums)