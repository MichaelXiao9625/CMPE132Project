from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

user_books = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

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

    books_checked_out = db.relationship('Book', secondary=user_books, backref=db.backref('checked_out_by', lazy='dynamic'))

    def has_checked_out(self, book_id):
        return any(book.id == book_id for book in self.books_checked_out)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))  # max 500 words
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Announcement {self.content[:50]}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default='Available')
    available_copies = db.Column(db.Integer, default=1)
    total_copies = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f"<Book '{self.title}' by {self.author}, Available Copies: {self.available_copies}/{self.total_copies}>"

class GuestUser(UserMixin):
    def __init__(self):
        self.id = 0  # Assign a unique identifier for the guest user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))