from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import Column, String, Integer, DateTime
from flask_login import UserMixin
from blog.database import Base


class Admin(Base, UserMixin):

    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    adminname = Column(String, unique=True)
    password_hash = Column(String)

    def __init__(self, adminname, password):
        self.adminname = adminname
        self.password = password

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_adminname(adminname):
        return Admin.query.filter_by(adminname=adminname).first()

    @staticmethod
    def get_by_id(id):
        return Admin.query.filter_by(id=id).first()


class Post(Base):

    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author = Column(String)
    date = Column(DateTime, default=datetime.utcnow())
    tag = Column(String)

    def __init__(self, title, content, author, tag):
        self.title = title
        self.content = content
        self.author = author
        self.tag = tag


class Tag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hit = Column(Integer)

    def __init__(self, name):
        self.name = name
        self.hit = 1