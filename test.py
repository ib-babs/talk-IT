from models import storage
from models.user import User
from models.comment import Comment
from models.post import Post
# import flask_tinymce

user = User()
comment = Comment()
question = Post()


storage.reload()
# # # from PIL import Image
# # # import base64
# # # from io import BytesIO

# # # with open('web_flask/static/image/avatar/woman.jpg', 'rb') as fp:
# # #     print(fp.raw.name.split('.')[-1])
# # #     #bytes = BytesIO(r)
# # #     #base64.b64encode(bytes.getvalue()).decode('utf-8')
# from flask_tinymce import TinyMCE

# print(TinyMCE)