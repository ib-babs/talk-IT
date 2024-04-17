#!/usr/bin/python3
from sqlalchemy import Column, String, ForeignKey, Boolean
from models.base_model import BaseModel, Base
'''PostLike subclass
Table to store the like of the post'''

class PostLike(BaseModel, Base):
    '''BaseModel and Base subclass'''
    __tablename__ = 'post_likes'
    post_id = Column(String(45), ForeignKey('posts.id'))
    user_id = Column(String(45), ForeignKey('users.id'))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
