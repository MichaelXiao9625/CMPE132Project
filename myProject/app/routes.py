from flask import render_template, redirect, url_for, request, Blueprint, session, flash, make_response
from sqlalchemy.exc import IntegrityError
from .models import User, Announcement, Book
from .forms import LoginForm, SignupForm, ProfileEditForm, Delete_Account_Form, AnnouncementForm, BookForm
import re
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route('/')   # routes to the base page
def base():
    view = request.args.get('view')  # Get the view parameter from URL
    return render_template("base.html", view=view)

@main.route('/guest-login')
def guest_login():
    session['is_guest'] = True  # Mark the session as guest
    return redirect(url_for('main.home'))

@main.route('/login', methods=['POST', 'GET'])  # routes to login page
def login():
    current_form = LoginForm()
    errorMessage = ''

    if current_form.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(username=current_form.username.data).first()

        if user and check_password_hash(user.password, current_form.password.data):
            # User exists and password is correct
            login_user(user, remember=current_form.remember_me.data)

            # Set a cookie for the last logged-in username if not a guest
            response = make_response(redirect('/home'))
            if user.role != 'guest':
                response.set_cookie('last_logged_in_username', current_form.username.data, max_age=30*24*60*60)  # 30 days expiration
            return response
        else:
            errorMessage = 'Invalid Username or Password'

    # Retrieve saved username from cookie, if available
    saved_username = request.cookies.get('last_logged_in_username', '')

    return render_template('login.html', form=current_form, error=errorMessage, saved_username=saved_username)

@main.route('/logout')
def logout():
    session.pop('is_guest', None)  # Remove guest flag from session
    response = make_response(redirect(url_for('main.base')))
    response.set_cookie('last_logged_in_username', '', expires=0)  # Clear the last logged-in username cookie
    logout_user()
    return response

@main.route('/delete_account', methods = ['POST', 'GET'])  #deletes account and routes to signup page
@login_required
def delete_account():

    current_form = Delete_Account_Form()
    user = User.query.filter_by(username=current_user.username).first()

    if current_form.validate_on_submit() and check_password_hash(user.password,current_form.password.data): #checking if password is correct
                    
        db.session.delete(user) #deleting user
        db.session.commit()
        return redirect('/signup')
            
    return render_template('delete_account.html', form = current_form, role=current_user.role)

@main.route('/home', methods=['POST', 'GET'])
def home():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    form = AnnouncementForm()  # Create a form instance
    if current_user.is_authenticated and current_user.role == 'admin':
        if form.validate_on_submit():
            new_announcement = Announcement(content=form.content.data)
            db.session.add(new_announcement)
            db.session.commit()
            return redirect(url_for('main.home'))  # Redirect after posting
        
        return render_template('home.html', role=current_user.role, announcements=announcements, form=form)
    elif current_user.is_authenticated and current_user.role == 'librarian':
        return render_template('home.html', role=current_user.role, announcements=announcements, form=form)
    elif current_user.is_authenticated and current_user.role == 'student':
        return render_template('home.html', role=current_user.role, announcements=announcements, form=form)
    elif session.get('is_guest'):
        # For guests, do not pass the form as they cannot create announcements
        return render_template('home.html', role='guest', announcements=announcements)
    else:
        return redirect(url_for('main.login'))

@main.route('/signup', methods=['POST', 'GET'])
def create():
    current_form = SignupForm()
    errorMessage = ''

    if current_form.validate_on_submit():
        existing_user = User.query.filter_by(email=current_form.email.data).first()
        if existing_user:
            errorMessage = 'An account with this email already exists.'
        elif not validPassword(current_form.password.data):
            errorMessage = 'Password must be longer than 8 characters, and contain at least one lowercase letter, one uppercase letter, one digit, and one special character'
        elif not validEmail(current_form.email.data):
            errorMessage = 'Invalid email address (must have domain .com, .org, .edu)'
        else:
            try:
                user = User()
                user.first = current_form.first.data
                user.last = current_form.last.data
                user.email = current_form.email.data
                user.username = current_form.username.data
                user.password = generate_password_hash(current_form.password.data)
                user.role = current_form.role.data
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            except IntegrityError:
                db.session.rollback()
                errorMessage = 'An account with this email or username already exists.'
    elif current_form.is_submitted():
        errorMessage = 'Please fill in all required fields'

    return render_template('signup.html', form=current_form, error=errorMessage)

# Create Announcement
@main.route('/create_announcement', methods=['GET', 'POST'])
@login_required
def create_announcement():
    # Only allow admin to access this page
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))

    form = AnnouncementForm()  # Assuming you have a form for this
    if form.validate_on_submit():
        announcement = Announcement(content=form.content.data)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('create_announcement.html', form=form)

# Edit Announcement
@main.route('/edit_announcement/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_announcement(id):
    # Only allow admin to access this page
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))

    announcement = Announcement.query.get_or_404(id)
    form = AnnouncementForm(obj=announcement)
    if form.validate_on_submit():
        announcement.content = form.content.data
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('edit_announcement.html', form=form, announcement=announcement)

# Delete Announcement
@main.route('/delete_announcement/<int:id>', methods=['POST'])
@login_required
def delete_announcement(id):
    # Only allow admin to access this page
    if current_user.role != 'admin':
        return redirect(url_for('main.home'))

    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    return redirect(url_for('main.home'))

from sqlalchemy import case

@main.route('/manage_users')
@login_required
def manage_users():
    # Retrieve all non-guest users
    users = User.query.filter(User.role != 'guest').all()

    # Define a custom order for roles
    role_priority = {'admin': 0, 'librarian': 1, 'student': 2}

    # Sort users based on role priority and then username
    sorted_users = sorted(users, key=lambda u: (role_priority.get(u.role, 3), u.username))

    return render_template('manage_users.html', users=sorted_users, role=current_user.role)

@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    errorMessage = ''
    user = User.query.get_or_404(user_id)
    if user.role == 'student':
        # Return all books checked out by the student
        for book in user.books_checked_out:
            book.available_copies += 1
    db.session.delete(user)
    db.session.commit()
    errorMessage = 'User has been deleted.'
    return redirect(url_for('main.manage_users', error=errorMessage))

@main.route('/user_profile/<int:user_id>')
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    checked_out_books = []
    if user.role == 'student':
        checked_out_books = user.books_checked_out
    return render_template('user_profile.html', user=user, checked_out_books=checked_out_books, role=current_user.role)

@main.route('/book_inventory')
def book_inventory():
    # Determine the role of the current user, default to 'guest' if not logged in
    role = current_user.role if current_user.is_authenticated else 'guest'

    # Redirect non-students, non-admins, and non-librarians if they are logged in
    if current_user.is_authenticated and role not in ['admin', 'librarian', 'student']:
        return redirect(url_for('main.home'))

    books = Book.query.all()
    return render_template('book_inventory.html', books=books, role=role)

@main.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role not in ['admin', 'librarian']:
        return redirect(url_for('main.home'))

    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('main.book_inventory'))

    return render_template('add_book.html', form=form, role=current_user.role)

@main.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    errorMessage = ''
    book = Book.query.get_or_404(book_id)
    # Remove the book from any users who have it checked out
    for user in User.query.all():
        if book in user.books_checked_out:
            user.books_checked_out.remove(book)
    
    db.session.delete(book)
    db.session.commit()
    errorMessage = 'Book successfully deleted.'
    return redirect(url_for('main.book_inventory', error=errorMessage))

@main.route('/update_copies/<int:book_id>', methods=['POST'])
@login_required
def update_copies(book_id):
    errorMessage = ''
    book = Book.query.get_or_404(book_id)
    action = request.form.get('action')

    if action == 'increase':
        book.total_copies += 1
        book.available_copies += 1
    elif action == 'decrease' and book.total_copies > 1:
        book.total_copies -= 1
        book.available_copies = max(book.available_copies - 1, 0)  # Ensure available copies don't go negative

    db.session.commit()
    errorMessage = 'Book copies updated successfully.'

    return redirect(url_for('main.book_inventory', error=errorMessage))

@main.route('/checkout_book/<int:book_id>', methods=['POST'])
@login_required
def checkout_book(book_id):
    errorMessage = ''
    book = Book.query.get_or_404(book_id)
    if book.available_copies > 0 and not current_user.has_checked_out(book_id):
        book.available_copies -= 1
        current_user.books_checked_out.append(book)  # Add book to the user's checked out books
        db.session.commit()
        errorMessage = 'You have successfully checked out the book.'
    else:
        flash('No copies available for checkout or you already have a copy.', 'danger')
    return redirect(url_for('main.book_inventory', error=errorMessage))

@main.route('/return_book/<int:book_id>/<return_page>', methods=['POST'])
@login_required
def return_book(book_id, return_page):
    errorMessage = ''
    book = Book.query.get_or_404(book_id)
    if book in current_user.books_checked_out:
        book.available_copies += 1
        current_user.books_checked_out.remove(book)
        db.session.commit()
        errorMessage = 'You have successfully returned the book.'
    else:
        flash('You cannot return a book you have not checked out.', 'danger')

    if return_page == 'my_books':
        return redirect(url_for('main.my_books', error=errorMessage))
    else:
        return redirect(url_for('main.book_inventory'))

@main.route('/profile')    #routes to current user profile page
@login_required
def test12():
    name= current_user.username
    bio = current_user.bio
    location = current_user.location
    email = current_user.email
    password = current_user.password
    dob = current_user.dob
    return render_template("profile.html", username=name, bio=bio, location=location, email=email, password=password, dob=dob, role=current_user.role)

@main.route('/profile_edit', methods=['POST', 'GET'])
@login_required
def profile_edit():
    current_form = ProfileEditForm()
    errorMessage = ''
    user = User.query.filter_by(username=current_user.username).first()

    if current_form.validate_on_submit():
        if len(current_form.bio.data) > 200:
            errorMessage = 'Bio is too long! (Max characters is 200)'
        else:
            # Concatenating the DOB fields
            dob_combined = f"{current_form.dob_year.data}-{current_form.dob_month.data}-{current_form.dob_day.data}"
            user.dob = dob_combined
            user.location = current_form.location.data
            user.bio = current_form.bio.data
            db.session.commit()
            return redirect('/profile')

    elif request.method == 'GET':
        # Pre-populate the form with existing data
        if user.dob:
            dob_parts = user.dob.split('-')
            current_form.dob_year.data = dob_parts[0]
            current_form.dob_month.data = dob_parts[1]
            current_form.dob_day.data = dob_parts[2]
        current_form.location.data = user.location
        current_form.bio.data = user.bio

    return render_template('profile_edit.html', form=current_form, error=errorMessage, role=current_user.role)

@main.route('/my_books', methods=['POST', 'GET'])
@login_required
def my_books():
    # Ensure only students can access this page
    if current_user.role != 'student':
        return redirect(url_for('main.home'))

    # Get the books checked out by the current user
    checked_out_books = current_user.books_checked_out

    return render_template('my_books.html', checked_out_books=checked_out_books, role=current_user.role)

@main.route('/help')
def help():
    role = current_user.role if current_user.is_authenticated else 'guest'
    return render_template('help.html', role=role)

# helper functions

class DataStore():  #class to store searched user
    searchedUser = None

data = DataStore()

def validPassword(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):  # Check for lowercase
        return False
    if not re.search("[A-Z]", password):  # Check for uppercase
        return False
    if not re.search("[0-9]", password):  # Check for digit
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):  # Check for special char
        return False
    return True

def validEmail(string): #checks if email is valid
    boolAddress = False
    boolDomain = False
    for i in string:
        if i == '@':
            boolAddress = True
    if (string[len(string)-4:len(string)] == '.com') or (string[len(string)-4:len(string)]) == '.org' or (string[len(string)-4:len(string)] == '.edu'):
        boolDomain = True
    return boolAddress and boolDomain
