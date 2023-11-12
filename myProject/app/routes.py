from flask import render_template, redirect, url_for, request, Blueprint, session
from sqlalchemy.exc import IntegrityError
from .models import User
from .forms import LoginForm, LogoutForm, SignupForm, SearchForm, SearchResult, ProfileEditForm, Delete_Account_Form
import re
from app import db
from datetime import date
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

@main.route('/login', methods=['POST', 'GET']) #routes to login page
def login():
    current_form = LoginForm()
    errorMessage = ''
    if current_form.validate_on_submit():   #checks once submit button is pressed
        users = User.query.all()  
        for user in users:
            if user.username == current_form.username.data: #checks if username is in database
                if check_password_hash(user.password,current_form.password.data): #checks if password is correct
                    if current_form.remember_me.data:
                        login_user(user, remember=True)
                    login_user(user, remember=current_form.remember_me.data) #logs in user
                    return redirect('/home')
            else:
                errorMessage = 'Invalid Username or Password'
    return render_template('login.html', form=current_form, error=errorMessage)

@main.route('/logout')
def logout():
    session.pop('is_guest', None)  # Remove guest flag from session
    logout_user()
    return redirect(url_for('main.base'))

@main.route('/delete_account', methods = ['POST', 'GET'])  #deletes account and routes to signup page
@login_required
def delete_account():

    current_form = Delete_Account_Form()
    user = User.query.filter_by(username=current_user.username).first()

    if current_form.validate_on_submit() and check_password_hash(user.password,current_form.password.data): #checking if password is correct
                    
        db.session.delete(user) #deleting user
        db.session.commit()
        return redirect('/signup')
            
    return render_template('delete_account.html', form = current_form)

@main.route('/home', methods=['POST', 'GET'])
def home():
    # Check if user is a guest
    if session.get('is_guest'):
        return render_template('home.html', role='guest')
    elif current_user.is_authenticated:
        return render_template('home.html', role=current_user.role)
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

@main.route('/search', methods = ['POST','GET'])   #routes to search page
def search():
    current_form = SearchForm()
    errormessage = ''
    if request.method == "GET": #before anything is entered show basic search html page
        return render_template('search.html', form = current_form)
    if request.method == "POST":    #after information is entered
        searched = request.form["username"] #finds what was entered in the search bar
        users = User.query.all()
        for user in users:
            if user.username == searched:   #if the searched username is found in the database
                data.searchedUser=searched   #store searched username             
                return redirect(url_for("user", usr=searched))  #redirect to user page
            else: 
                errormessage = 'User not found'  
    return render_template('search.html', error = errormessage)

@main.route('/user/<usr>', methods = ['POST','GET'])   #usr url is the searched username
def user(usr):
    current_form = SearchResult()
    return render_template('searchResult.html', form=current_form, username=usr)

@main.route('/profile')    #routes to current user profile page
@login_required
def test12():
    name= current_user.username
    bio = current_user.bio
    location = current_user.location
    email = current_user.email
    password = current_user.password
    dob = current_user.dob
    return render_template("profile.html", username=name, bio=bio, location=location, email=email, password=password, dob=dob)

@main.route('/profile_edit', methods = ['POST','GET']) #routes to profile edit page
@login_required
def profile_edit():
    current_form = ProfileEditForm()
    errorMessage = ''
    user = User.query.filter_by(username=current_user.username).first() #retreiving current user
    if current_form.validate_on_submit():

        if len(current_form.bio.data) > 200:
            errorMessage = 'Bio is too long! (Max characters is 200)'
           
        else:
            user.dob = current_form.dob.data            #updating dob, location, and bio of user
            user.location = current_form.location.data
            user.bio = current_form.bio.data
            db.session.add(user)
            db.session.commit()
            return redirect('/profile') #redirects to profile after submitting form, will show updated bio, dob, location
    return render_template('profile_edit.html', form=current_form, error = errorMessage)


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
