from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
import os
import secrets

from .models import db, User, Role

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(app.instance_path, 'music.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', secrets.token_hex(16))
    app.config['SECURITY_REGISTERABLE'] = True
    app.config['SECURITY_SEND_REGISTER_EMAIL'] = False  # Disable email for now
    app.config['UPLOAD_FOLDER'] = os.path.join('music/static', 'uploads')

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database and migration tool
    db.init_app(app)
    migrate = Migrate(app, db)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()  # Create tables

        # Create roles if they don't exist
        if not user_datastore.find_role("admin"):
            user_datastore.create_role(name="admin", description="Administrator role")
        if not user_datastore.find_role("user"):
            user_datastore.create_role(name="user", description="Regular user role")

        # Create test user if doesn't exist
        if not user_datastore.find_user(email="admin@example.com"):
            admin_role = user_datastore.find_role("admin")
            user = user_datastore.create_user(
                email="admin@example.com",
                password="password"  # hashed automatically by Flask-Security
            )
            user_datastore.add_role_to_user(user, admin_role)
            db.session.commit()

    # Test route
    @app.route("/")
    def hello():
        return render_template('base.html')
    
    #registring song blueprint
    from . import song
    app.register_blueprint(song.song_bp)

    return app
