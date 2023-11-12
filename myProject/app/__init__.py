from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate  # Import Flask-Migrate

myapp_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.update(
    SECRET_KEY='secret',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
db = SQLAlchemy(myapp_obj)

# Initialize Flask-Migrate
migrate = Migrate(myapp_obj, db)

login = LoginManager(myapp_obj)

login.login_view = 'login'

from app import routes, models
