from enums.user import UserEnum
from model.setup.sql_imports import *
from model.table.hotel import Hotel


class User(db.Model):
    __tablename__ = 'user'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), unique=True, nullable=False)
    birthday = Column(DateTime)
    is_admin = Column(Boolean, nullable=False)
    is_bot = Column(Boolean, nullable=False)
    permission = Column(Enum(UserEnum))
    location_link = Column(String(500))
