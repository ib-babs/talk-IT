from flask import Flask
from io import BytesIO
from PIL import Image
import base64
import os
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd5a069af3ae4427a626206'
app.config['DATABASE'] = 'mysql+mysqldb'

login_manager = LoginManager()
login_manager.init_app(app)


def save_image_to_db(image_file=None, is_file_storage=True, img_fmt=True):
    if is_file_storage and img_fmt:
        image_path = os.path.join(
            os.getcwd(), f'web_flask/static/image/avatar/{image_file}')
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


# def buffer_image(user):
#     # Validate user
#     img_base = 'None'
#     img_format = 'None'

#     if user and user.image:
#         img = Image.open(BytesIO(user.image))
#         img.thumbnail((300, 300))
#         buffered = BytesIO()
#         img_format = img.format.lower()
#         img.save(buffered, format=f'{img_format}')
#         img_base = base64.b64encode(buffered.getvalue()).decode('utf-8')
#     return (img_base, img_format)
