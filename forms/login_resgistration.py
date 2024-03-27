#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField, SelectField


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
    gender = SelectField(choices=[
                         'Male', 'Female', "I'd rather not say."], default="I'd rather not say.", name='gender')
    signup = SubmitField('Sign Up', id='submit-btn')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[
                             DataRequired()], render_kw={'placeholder': 'Password'})
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
