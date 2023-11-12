from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class HomePageForm(FlaskForm):
    submitHome = SubmitField('Home')
    
class LogoutForm(FlaskForm):
    submitLogout = SubmitField('Logout')

class SignupForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])

    role = RadioField('Role', choices=[('admin', 'Admin'), ('librarian', 'Librarian'), ('student', 'Student')])
    submit = SubmitField('Create Account')

class SearchForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Search')

class SearchResult(FlaskForm):
    username = StringField('Username')

class ProfileEditForm(FlaskForm):
    dob = StringField('yyyy-mm-dd')
    location = StringField('Location')
    bio = StringField('Bio')
    submit = SubmitField('Save')

class ProfileForm(FlaskForm):
    submit= SubmitField('Profile')

class Delete_Account_Form(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Delete Account')
