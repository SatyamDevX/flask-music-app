from flask import Blueprint, render_template, request, current_app

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

      #Enuser upload folder extist
      # os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
      filename = secure_filename(file.filename)
      save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
      file.save(save_path)
      print(f"Saving to: {save_path}")

      
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


