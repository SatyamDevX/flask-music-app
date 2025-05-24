from flask import Blueprint, render_template, request, current_app, redirect, url_for, jsonify

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user, login_required, roles_required

import os


from music.models import db, Song, Playlist, PlaylistSong, Album


album_bp = Blueprint('album', __name__, url_prefix='/album')

@album_bp.route('/create', methods=['POST'])
@login_required
@roles_required('admin')
def create_album():
   title = request.form['title']
   if not title:
    return jsonify({'error': 'Title is required'}), 400

   new_album = Album(title=title, creator_id=current_user.id)
   db.session.add(new_album)
   db.session.commit()

   # return jsonify({'message': 'Album created', 'album_id': new_album.id}), 201
   return redirect(request.referrer)




@album_bp.route('/add_song_to_album/page', methods=['GET','POST'])
@login_required
@roles_required('admin')
def add_song_to_album_page():
  albumid=request.args.get("album_id")
  albumtitle=request.args.get("album_title")
#   print(albumid,albumtitle)
  songs=Song.query.all()
  return render_template('all_song.html', songs=songs, albumid=albumid, albumtitle=albumtitle)

@album_bp.route('/add_song_to_album', methods=['GET','POST'])
@login_required
@roles_required('admin')
def add_song_to_album():
   album_id=request.args.get("album_id")
   song_id=request.args.get("song_id")
   print(album_id,song_id)


   song = Song.query.get(song_id)
   if not song:
      return "Song not found", 404

   if not album_id:
      return "No album selected or created", 400

   album = Album.query.get(album_id)
   if album.creator_id != song.creator_id:
      return "Only the creator can assign a song to this album", 403

   song.album_id = album_id
   db.session.commit()

   return "Song added to album", 200

@album_bp.route('/songs')
@login_required
@roles_required('admin')
def album_songs():
   album_id=request.args.get('album_id')
   album = Album.query.get_or_404(album_id)
   songs = album.songs  # This uses the relationship in your model
   return render_template('album_song.html', album=album, songs=songs)
  



