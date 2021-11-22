from model.setup.sql_imports import *
from model.table.hotel import Hotel


class Apartment(db.Model):
    __tablename__ = 'apartment'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    hotel_id = Column(INTEGER, ForeignKey('hotel.id'))
    image = Column(String(500))
    room_capacity = Column(INTEGER, nullable=False)
    # room_type = Column()  # EEEEEEE
    floor = Column(INTEGER, nullable=False)
    cost = Column(INTEGER, nullable=False)
    description = Column(String(750))
