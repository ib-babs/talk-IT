#!/usr/bin/python3
from typing import Any
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
import sqlalchemy
from web_flask import timeConversion
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
time = "%Y-%m-%d %H:%M:%S.%f"


class BaseModel:
    id = Column(String(45), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):

        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
                if kwargs.get('id') is None:
                    self.id = str(uuid4())
                if kwargs.get('created_at') and type(kwargs['created_at']) is str:
                    self.created_at = datetime.strptime(
                        str(datetime.now()), time)
                # else:
                #     self.created_at = datetime.now()
                if kwargs.get('updated_at') and type(kwargs['updated_at']) is str:
                    self.updated_at = datetime.strptime(
                        str(datetime.now()), time)
                # else:
                #     self.updated_at = datetime.now()
        else:
            self.id = str(uuid4())
            self.created_at = datetime.strptime(str(datetime.now()), time)
            self.updated_at = self.created_at

    def to_dict(self):
        new_dict = self.__dict__.copy()
        if 'created_at' in new_dict:
            new_dict['created_at'] = new_dict['created_at'].strftime(time)
        if 'updated_at' in new_dict:
            new_dict['updated_at'] = new_dict['updated_at'].strftime(time)

        if not 'created_at_time' in new_dict:
            new_dict['created_at_time'] = timeConversion(
                new_dict['created_at'])
        if not 'updated_at_time' in new_dict:
            new_dict['updated_at_time'] = timeConversion(
                new_dict['updated_at'])

        if '__class__' in new_dict:
            new_dict['__class__'] = self.__class__.__name__
        if 'password' in new_dict:
            del new_dict['password']
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        if 'image' in new_dict:
            del new_dict['image']
        return new_dict

    def __str__(self) -> str:
        return '[{}.{}] {}'.format(self.__class__.__name__, self.id, self.to_dict())
