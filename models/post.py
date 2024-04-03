#!/usr/bin/python3
from sqlalchemy import Column, String, Text, ForeignKey, Integer, Boolean
from models.base_model import BaseModel, Base


class Post(BaseModel, Base):
    __tablename__ = 'posts'
    title = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    user_id = Column(String(45), ForeignKey('users.id'),
                     nullable=False)
    has_liked = Column(Boolean, default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
