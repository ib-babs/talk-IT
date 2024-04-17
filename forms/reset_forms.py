#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from wtforms import EmailField, PasswordField, SubmitField
from models import storage
from models.user import User
'''Password reseting module'''


class RequestResetForm(FlaskForm):
    '''Request Reset form'''
    email = EmailField(validators=[
                       DataRequired(), Length(10, 100)], name='email', id='email',
                       render_kw={'placeholder': 'Email'})
    submit = SubmitField('Request Reset Password', id='request-reset-pwd-btn')

    # Validating an email provided by the user
    def validate_email(self, email):
        user = storage.get_user_by_email(User, email.data)
        if user is None:
            raise ValidationError(
                'There is no account with this email!')


class ResetPasswordForm(FlaskForm):
    '''Resetting password form'''
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

    submit = SubmitField('Done', id='reset-pwd-btn')
