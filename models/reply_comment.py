#!/usr/bin/python3
from sqlalchemy import Column, String, Text, ForeignKey
from models.base_model import BaseModel, Base


class Reply(BaseModel, Base):
    __tablename__ = 'replies'
    content = Column(Text, nullable=False)
    user_id = Column(String(45), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    comment_id = Column(String(45), ForeignKey(
        'comments.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
