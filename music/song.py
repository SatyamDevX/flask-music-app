from flask import Blueprint, render_template, request, current_app, redirect, url_for

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user, login_required

import os


from music.models import db, Song, Playlist, PlaylistSong


song_bp = Blueprint('song', __name__, url_prefix='/song')

@song_bp.route('/all')
def song_all():
   songs = Song.query.all()
   return render_template('song_list.html', songs=songs)


@song_bp.route('/upload', methods=('GET','POST'))
@login_required
def song_upload():
   if request.method == 'POST':
      title = request.form['title']
      artist = request.form['artist']
      file = request.files['file']
      filename = file.filename
      lrcfile = request.files['lrcfile']
      original_lrcfilename = lrcfile.filename

      #Enuser upload folder extist
      # os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
      filename = secure_filename(file.filename)
      save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
      file.save(save_path)
      print(f"Saving to: {save_path}")

      lrcfilename = filename[:-4] + ".lrc"
      lrc_save_path = os.path.join(current_app.config['LRC_UPLOAD_FOLDER'], lrcfilename)
      lrcfile.save(lrc_save_path)
      print(lrc_save_path)
      
      # Save song info in DB
      song = Song(
            title=title,
            artist=artist,
            file_path=filename,  # Only filename; path handled by Flask
            creator_id=current_user.id  # assumes user is logged in
            # creator_id=2
      )
      db.session.add(song)
      db.session.commit()


      print(title, artist, filename)
   return render_template('song_upload.html')


@song_bp.route('/<int:song_id>/delete', methods=["GET","POST"])
@login_required
def delete_song(song_id):

   song=Song.query.get(song_id)
   #file_path=upload_folderpath+filename
   file_path=os.path.join(current_app.config['UPLOAD_FOLDER'], song.file_path)
   os.remove(file_path)

   db.session.delete(song)
   db.session.commit()
   return redirect('/song/all')

@song_bp.route('/<int:song_id>/play')
def play_song(song_id):
   song=Song.query.get(song_id)
   print(song)
   return render_template("song_play.html",s=song)


@song_bp.route('/add_song_to_playlist/<int:song_id>', methods=['GET'])
@login_required
def show_add_to_playlist_form(song_id):

   playlists = Playlist.query.filter_by(user_id=current_user.id).all()
   return render_template('add_song_playlist.html', playlists=playlists, song_id=song_id)


@song_bp.route('/add_song_to_playlist', methods=['POST'])
@login_required
def add_song_to_playlist():
    song_id = request.form.get('song_id')
    playlist_id = request.form.get('playlist_id')
    new_name = request.form.get('new_playlist_name')

    song = Song.query.get(song_id)
    if not song:
        return "Song not found", 404

    # Create new playlist if needed
    if not playlist_id and new_name:
        new_playlist = Playlist(name=new_name, user_id=current_user.id)
        db.session.add(new_playlist)
        db.session.commit()
        playlist_id = new_playlist.id

    if not playlist_id:
        return "No playlist selected or created", 400

    # Check for duplicate
    exists = PlaylistSong.query.filter_by(playlist_id=playlist_id, song_id=song_id).first()
    if exists:
        return "Song already in playlist", 409

    # Add song to playlist
    new_link = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
    db.session.add(new_link)
    db.session.commit()

    return redirect(url_for('song.show_add_to_playlist_form', song_id=song_id))

