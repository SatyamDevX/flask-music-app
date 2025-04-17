from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
import uuid

db = SQLAlchemy()

# Association table for User ↔ Role
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    active = db.Column(db.Boolean, default=True)  # Default is active (True)
    password = db.Column(db.String(256), nullable=False)
    is_creator = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    playlists = db.relationship('Playlist', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    songs_uploaded = db.relationship('Song', backref='creator', lazy=True)
    albums_created = db.relationship('Album', backref='creator', lazy=True)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100))
    file_path = db.Column(db.String(300), nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

    ratings = db.relationship('Rating', backref='song', lazy=True)
    playlists = db.relationship('PlaylistSong', back_populates='song')


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    songs = db.relationship('PlaylistSong', back_populates='playlist')


# Association table for Playlist ↔ Song (Many-to-Many)
class PlaylistSong(db.Model):
    __tablename__ = 'playlist_song'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)

    playlist = db.relationship('Playlist', back_populates='songs')
    song = db.relationship('Song', back_populates='playlists')


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    songs = db.relationship('Song', backref='album', lazy=True)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)  # 1 to 5
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
