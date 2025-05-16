from flask import Blueprint, render_template, request, current_app, redirect

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user

import os


from music.models import db, Song


song_bp = Blueprint('song', __name__, url_prefix='/song')

@song_bp.route('/all')
def song_all():
   songs = Song.query.all()
   return render_template('song_list.html', songs=songs)


@song_bp.route('/upload', methods=('GET','POST'))
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
            # creator_id=current_user.id  # assumes user is logged in
            creator_id=2
      )
      db.session.add(song)
      db.session.commit()


      print(title, artist, filename)
   return render_template('song_upload.html')


@song_bp.route('/<int:song_id>/delete', methods=["GET","POST"])
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
