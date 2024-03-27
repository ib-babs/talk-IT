#!/usr/bin/python3
from sqlalchemy import Column, String, Text, Numeric, ForeignKey
from models.base_model import BaseModel, Base


class Answer(BaseModel, Base):
    __tablename__ = 'answers'
    comment = Column(Text, nullable=False)
    like = Column(Numeric, nullable=False, default=0)
    user_id = Column(String(45), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(String(45), ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
