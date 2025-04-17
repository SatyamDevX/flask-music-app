from flask import Flask, render_template
from .models import db
import os

def create_app():
   app = Flask(__name__, instance_relative_config=True)

   # Configuration
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'music.db')
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

   # Ensure instance folder exists
   try:
      os.makedirs(app.instance_path)
   except OSError:
      pass

   # Initialize database
   db.init_app(app)

   with app.app_context():
      db.create_all()

   # Test route
   @app.route("/")
   def hello():
      return render_template('home.html')

   return app
