#!/usr/bin/python3
from flask import Flask, url_for
from io import BytesIO
from PIL import Image
import base64
import os
from flask_login import LoginManager
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True  # or False for SSL
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Mail Manager
mail = Mail(app)

# Send user a reset password email message


def send_reset_email(user):
    '''Send reset email message'''
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=os.getenv('EMAIL_USER'), recipients=[
                  user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
Ignore the message if you don't request for password reset and no change will be made!'''
    mail.send(msg)
    return 'Email is sent successfully!'


def save_image_to_db(image_file=None, is_file_storage=True, img_fmt=True):
    if is_file_storage and img_fmt:
        image_path = os.path.join(
            os.getcwd(), f'talk-IT/web_flask/static/image/avatar/{image_file}')
        with open(image_path, 'rb') as fp:
            img_format = fp.raw.name.split('.')[-1]
            bytes = BytesIO(fp.read())
            return (base64.b64encode(bytes.getvalue()).decode('utf-8'), img_format)
    if is_file_storage is False and img_fmt is True:
        img = Image.open(BytesIO(image_file.read()))
        img.thumbnail((300, 300))
        image_fmt = img.format.lower()
        buffered = BytesIO()
        img.save(buffered, format=f'{image_fmt}')
        return (base64.b64encode(buffered.getvalue()).decode('utf-8'), image_fmt)


def timeConversion(time_given):
    '''Convert time object to year | day | hour | minute | second '''
    from datetime import datetime

    # Your given date
    given_date = datetime.strptime(time_given, "%Y-%m-%d %H:%M:%S.%f")

    # Current date
    current_date = datetime.now()

    # Calculate the difference in seconds
    difference = (current_date - given_date).total_seconds()

    # Define the time intervals in seconds
    intervals = {
        'yr': 365 * 24 * 60 * 60,
        'day': 24 * 60 * 60,
        'hr': 60 * 60,
        'min': 60,
        'second': 1
    }

    # Initialize an empty list to store the time ago components
    time_components = []

    # Calculate the time ago for each interval
    for name, count in intervals.items():
        value = int(difference // count)
        if value:
            time_components.append(
                f"{value} {'year' if name == 'year' else name + 's'}" if name == 'year' else f"{value}{name+'s' if value > 1 else name}")
            difference %= count

    # Construct the time ago string
    find_time = ''.join(time_components[0]) + \
        ' ago' if time_components else 'Just now'
    return find_time
