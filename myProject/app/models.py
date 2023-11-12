from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first = db.Column(db.String)
    last = db.Column(db.String)
    email = db.Column(db.String(32), unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(10))

    bio = db.Column(db.String)
    dob = db.Column(db.String)
    location = db.Column(db.String) 

class GuestUser(UserMixin):
    def __init__(self):
        self.id = 0  # Assign a unique identifier for the guest user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))