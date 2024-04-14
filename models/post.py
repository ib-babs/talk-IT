#!/usr/bin/python3
from sqlalchemy import Column, String, Text, ForeignKey, Integer, JSON
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class Post(BaseModel, Base):
    __tablename__ = 'posts'
    post = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    user_id = Column(String(45), ForeignKey('users.id'),
                     nullable=False)
    post_images = Column(JSON)
    post_like_id = relationship(
        'PostLike', backref='post',  cascade="all, delete")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
