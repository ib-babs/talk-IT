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


# Twitter sharing link - https://twitter.com/share?url=127.0.0.1%3A5500%2Fhttp%3A%2F%2F127.0.0.1%3A6522%2Fread_post%2Fb920cb02-f7dc-4042-973a-2e6132933327&text=Three%20Muskeeter

# Facebook - https://facebook.com/sharer/sharer.php?u=127.0.0.1%3A5500%2Fhttp%3A%2F%2F127.0.0.1%3A6522%2Fread_post%2Fb920cb02-f7dc-4042-973a-2e6132933327

# Linkedin - https://www.linkedin.com/shareArticle?mini=true&url=127.0.0.1%3A5500%2Fhttp%3A%2F%2F127.0.0.1%3A6522%2Fread_post%2Fb920cb02-f7dc-4042-973a-2e6132933327

# WhatsApp - whatsapp://send?text=127.0.0.1%3A5500%2Fhttp%3A%2F%2F127.0.0.1%3A6522%2Fread_post%2Fb920cb02-f7dc-4042-973a-2e6132933327%20Three%20Muskeeter

# Telegram - tg://msg?text=127.0.0.1%3A5500%2Fhttp%3A%2F%2F127.0.0.1%3A6522%2Fread_post%2Fb920cb02-f7dc-4042-973a-2e6132933327%20Three%20Muskeeter
