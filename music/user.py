from flask import Blueprint, render_template, request, current_app, redirect

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user

import os


from music.models import db, Song


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard')
def userdashboard():
   songs = Song.query.all()
   return render_template('user_dashboard.html', songs=songs)



