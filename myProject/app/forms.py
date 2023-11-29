from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
import calendar

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    
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

class AnnouncementForm(FlaskForm):
    content = TextAreaField('Announcement', validators=[
        DataRequired(),
        Length(max=500, message='Announcement must be less than 500 characters.')  # Limit the length of an announcement
    ])
    submit = SubmitField('Post Announcement')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Add Book')

class ProfileEditForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(max=200)])

    # Dropdown fields for Date of Birth
    dob_day = SelectField('Day', choices=[('', 'Day')] + [(str(day), str(day)) for day in range(1, 32)], validators=[DataRequired()])
    dob_month = SelectField('Month', choices=[('', 'Month')] + [(str(i), calendar.month_name[i]) for i in range(1, 13)], validators=[DataRequired()])
    dob_year = SelectField('Year', choices=[('', 'Year')] + [(str(year), str(year)) for year in range(1950, 2051)], validators=[DataRequired()])

    location = StringField('Location')
    submit = SubmitField('Save')

class ProfileForm(FlaskForm):
    submit= SubmitField('Profile')

class Delete_Account_Form(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Delete Account')
