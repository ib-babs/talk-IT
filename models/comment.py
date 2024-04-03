#!/usr/bin/python3
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from models.base_model import BaseModel, Base


class Comment(BaseModel, Base):
    __tablename__ = 'comments'
    comment = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    user_id = Column(String(45), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(String(45), ForeignKey(
        'posts.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
