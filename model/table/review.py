from model.setup.sql_imports import *
from model.table.user import User
from model.table.hotel import Hotel


class Review(db.Model):
    __tablename__ = 'review'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    hotel_id = Column(INTEGER, ForeignKey('hotel.id'))
    user_id = Column(INTEGER, ForeignKey('user.id'))
    review = Column(String(500), nullable=True)
    mark = Column(INTEGER, nullable=False)
