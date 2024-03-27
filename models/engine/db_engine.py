#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.question import Question
from models.answer import Answer
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, 'Question': Question, 'Answer': Answer}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        TALK_IT_MYSQL_USER = getenv('TALK_IT_MYSQL_USER')
        TALK_IT_MYSQL_PWD = getenv('TALK_IT_MYSQL_PWD')
        TALK_IT_MYSQL_HOST = getenv('TALK_IT_MYSQL_HOST')
        TALK_IT_MYSQL_DB = getenv('TALK_IT_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(TALK_IT_MYSQL_USER,
                                             TALK_IT_MYSQL_PWD,
                                             TALK_IT_MYSQL_HOST,
                                             TALK_IT_MYSQL_DB))

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Return one object or `None` if not found"""
        objects = self.__session.query(cls)
        for obj in objects:
            if obj.id == id:
                return obj
        return None

    def get_questions(self, cls, user_id):
        """Return all question objects based on user_id"""
        objects = self.__session.query(cls).filter(
            cls.user_id == user_id).all()
        if objects:
            question_objects = [obj for obj in objects]
            return question_objects
        return None

    def get_user(self, cls, username):
        """Return one user object or `None` if not found"""
        objects = self.__session.query(cls).filter(
            cls.username == username).all()
        if objects is not None:
            for obj in objects:
                # if obj.id == id:
                return obj
        return None

    def get_other_question(self, cls, id):
        """Return all question object without the current_user's or `None` if not found"""
        objects = self.__session.query(Question, cls).join(cls).filter(
            cls.id != id).all()
        if objects:
            return objects
        return None

    def get_comments(self, cls, question_id):
        """Return all comment object or `None` if not found"""
        objects = self.__session.query(User, cls).\
            join(Question, cls.post_id == Question.id).\
            join(User, cls.user_id == User.id).filter(
            cls.post_id == question_id).all()
        if objects:
            return objects
        return None

    def count(self, cls=None):
        """Return the number of objects in storage"""
        total = 0
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                total += len(self.__session.query(classes[clss]).all())
        return total
