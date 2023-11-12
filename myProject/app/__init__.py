# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config.update(
        SECRET_KEY='secret',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    login.init_app(app)
    Migrate(app, db)

    login.login_view = 'main.login'  # Updated to use Blueprint

    from .routes import main as main_routes
    app.register_blueprint(main_routes)

    return app
