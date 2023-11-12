from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash

def add_guest_user():
    app = create_app()
    with app.app_context():
        # Check if guest user already exists
        guest_user = User.query.filter_by(username='guest').first()
        if not guest_user:
            guest_user = User(
                username='guest',
                password=generate_password_hash('guest'),  # Or some dummy password
                role='guest',
                # Leave other fields blank or fill in as necessary
            )
            db.session.add(guest_user)
            db.session.commit()
            print("Guest user added.")
        else:
            print("Guest user already exists.")

if __name__ == '__main__':
    add_guest_user()
