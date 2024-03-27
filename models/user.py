#!/usr/bin/python3
from sqlalchemy import Column, String, Text
from models.base_model import BaseModel, Base
from hashlib import md5
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    __tablename__ = 'users'
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    username = Column(String(45), nullable=False, unique=True)
    image = Column(Text)
    image_fmt = Column(Text)
    gender = Column(String(20), nullable=True)
    question_id = relationship('Question', backref='user',  cascade="all, delete")
    comment_id = relationship('Answer', backref='user',  cascade="all, delete")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.password is not None:
            self.password = md5(str(self.password).encode('utf-8')).hexdigest()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
