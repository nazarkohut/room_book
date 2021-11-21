from datetime import timedelta

from flask_jwt_extended import create_access_token

from enums.user import UserEnum
from model.setup.sql_imports import *
from model.table.hotel import Hotel
from passlib.hash import bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), unique=False, nullable=False)
    birthday = Column(DateTime, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_bot = Column(Boolean, nullable=False, default=False)
    hotel_owner = Column(Boolean, nullable=False, default=False)
    location_link = Column(String(500), nullable=True)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.username = kwargs.get('username')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.birthday = kwargs.get('birthday')
        self.is_admin = kwargs.get('is_admin')
        self.is_bot = kwargs.get('is_bot')
        self.hotel_owner = kwargs.get('hotel_owner')
        self.location_link = kwargs.get('location_link')

    def get_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token
