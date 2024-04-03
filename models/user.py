#!/usr/bin/python3
from sqlalchemy import Column, String, Text, Integer
from models.base_model import BaseModel, Base
from hashlib import md5
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from web_flask import app


class User(BaseModel, Base, UserMixin):
    __tablename__ = 'users'
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    followers = Column(Integer, default=0)
    image = Column(Text)
    image_fmt = Column(Text)
    gender = Column(String(20), nullable=True)
    question_id = relationship(
        'Post', backref='user',  cascade="all, delete")
    comment_id = relationship(
        'Comment', backref='user',  cascade="all, delete")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.password is not None:
            self.password = md5(str(self.password).encode('utf-8')).hexdigest()

    def get_reset_token(self, expire_sec=1800):
        '''Reset password'''
        s = Serializer(app.config['SECRET_KEY'], expires_in=expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(storage, cls, token):
        '''Verifying token'''
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return storage.get(cls, user_id)

    # # def is_authenticated(self):
    # #     return True

    # # def is_active(self):
    # #     return True

    # # def is_anonymous(self):
    # #     return False

    # # def get_id(self):
    # #     return str(self.id)
