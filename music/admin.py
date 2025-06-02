from flask import Blueprint, render_template, request, current_app, redirect, flash, url_for

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from flask_security import current_user, login_required, roles_required

import os


from music.models import db, Song, PlaylistSong, Playlist, Album, User, Role
from sqlalchemy.orm import joinedload

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route('/dashboard')
@login_required
def admind_ashboard():
   songs = Song.query.all()
   albums = Album.query.all()

   return render_template("admin_dashboard.html", albums=albums, songs=songs)

@admin_bp.route('/approve_creators')
@roles_required('admin')  # Flask-Security decorator
def approve_creators():
    pending_users = User.query.filter_by(creator_requested=True, is_creator=False).all()
    approved_users = User.query.filter_by(is_creator=True).all()
    return render_template('approve_creators.html', users=pending_users, creators=approved_users)

@admin_bp.route('/block_creator/<int:user_id>', methods=['POST'])
@admin_bp.route('/approve_creator/<int:user_id>', methods=['POST'])
@roles_required('admin')
def approve_creator_action(user_id):
    user = User.query.get_or_404(user_id)
    creator_role = Role.query.filter_by(name='creator').first()

    if not creator_role:
        creator_role = Role(name='creator', description='Creator role')
        db.session.add(creator_role)
        db.session.commit()
    if user.is_creator:
        user.roles.remove(creator_role)
        user.is_creator = False
        db.session.commit()
        flash(f"{user.username} has been Blocked as a creator.", 'success')
        return redirect(url_for('admin.approve_creators'))
    else:
        user.roles.append(creator_role)
        user.is_creator = True
        user.creator_requested = False
        db.session.commit()

        flash(f"{user.username} has been approved as a creator.", 'success')
        return redirect(url_for('admin.approve_creators'))

