#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.post import Post
from models.post_like import PostLike
from models.comment import Comment
from models.reply_comment import Reply
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User, 'Post': Post,
           'Comment': Comment, 'Postlike': PostLike, 'Reply': Reply}


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

    def get_posts(self, cls, user_id):
        """Return all post objects based on user_id"""
        objects = self.__session.query(cls).filter(
            cls.user_id == user_id).all()
        if objects:
            post_objects = [obj for obj in objects]
            return post_objects
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

    def get_other_post(self, cls, id):
        """Return all post object without the current_user's or `None` if not found"""
        objects = self.__session.query(Post, cls).join(cls).filter(
            cls.id != id).all()
        if objects:
            return objects
        return None

    def get_all_posts_and_users(self, cls):
        """Return all post or `None` if not found"""
        objects = self.__session.query(Post, cls).join(cls).all()
        return objects or None

    def get_comments(self, cls, post_id):
        """Return all comment object or `None` if not found"""
        objects = self.__session.query(User, cls).\
            join(Post, cls.post_id == Post.id).\
            join(User, cls.user_id == User.id).filter(
            cls.post_id == post_id).all()
        if objects:
            return objects
        return None

    def get_user_by_email(self, cls, email):
        obj = self.__session.query(cls).filter(
            cls.email == email).first() or None
        return obj

    def count(self, cls=None):
        """Return the number of objects in storage"""
        total = 0
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                total += len(self.__session.query(classes[clss]).all())
        return total

    def count_comment_or_like(self, cls, post_id=None):
        """Return the number of comment in storage based on post_id"""
        obj_total = self.__session.query(cls).filter(
            cls.post_id == post_id).all() or None
        if obj_total:
            return len(obj_total)
        return 0
    def count_reply(self, cls, comment_id=None):
        """Return the number of reply in storage based on comment_id"""
        obj_total = self.__session.query(cls).filter(
            cls.comment_id== comment_id).all() or None
        if obj_total:
            return len(obj_total)
        return 0
