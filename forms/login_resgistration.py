#!/usr/bin/python3
from models.user import User
from models import storage
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField, SelectField, BooleanField


class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name:', validators=[
        DataRequired(), Length(3, 100)], id='fullname',
        name='fullname', render_kw={'placeholder': 'Full Name'})
    username = StringField('Username:', validators=[
        DataRequired(), Length(4, 45)], name='username', id='username',
        render_kw={'placeholder': 'Username'})
    email = EmailField(validators=[
                       DataRequired(), Length(10, 100)], name='email', id='email',
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password:', validators=[
                             DataRequired(), Length(8, 16)], name='password', id='password',
                             render_kw={'placeholder': 'Password'})
    confirm_password = PasswordField('Confirm Password:', validators=[
                                     DataRequired(),  EqualTo('confirm_password', message='Password must match')],
                                     name='confirm_password', id='confirm_password',
                                     render_kw={'placeholder': 'Confirm Password'})

    # Validate Password and Confirm password field
    def validate_confirm_password(self, confirm_password):
        if confirm_password.data != self.password.data:
            raise ValidationError('Password does not match!')

    # Validating email
    def validate_email(self, email):
        if storage.get_user_by_email(User, email.data):
            raise ValidationError(
                'Email is already taken.')

    # Validating username
    def validate_username(self, username):
        if storage.get_user(User, username.data):
            raise ValidationError(
                f'Username is already exist!')

    gender = SelectField(choices=[
                         'Male', 'Female', "Rather not say"], default="Rather not say", name='gender')
    signup = SubmitField('Sign Up', id='submit-btn')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[
                             DataRequired()], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Remeber Me', id='remember_me')
    sign_in = SubmitField('Sign in')


class LogOutForm(FlaskForm):
    logout = SubmitField('Log out', id='logout', name='logout')


class UpdateProfile(FlaskForm):
    full_name = StringField('Full Name:', validators=[
        DataRequired(), Length(3, 100)], id='full_name',
        name='full_name', render_kw={'placeholder': 'Full Name'})
    username = StringField('Username:', validators=[
        DataRequired(), Length(4, 45)], name='username', id='username',
        render_kw={'placeholder': 'Username'})
    email = EmailField(validators=[
                       DataRequired(), Length(10, 100)], name='email', id='email',
                       render_kw={'placeholder': 'Email'})
    image = FileField('Update Picture:',
                      name='image', id='image', render_kw={'accept': 'image/*'})
    gender = SelectField(choices=[
                         'Male', 'Female', "I'd rather not say."], default="I'd rather not say.", name='gender')
    submit = SubmitField('Submit', id='edit-profile-btn',
                         name='edit-profile-btn')
