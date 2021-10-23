from sqlalchemy import ForeignKey, INTEGER, Column, String, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship

from app import db
from enums.hotel import BreakfastEnum, TransportEnum
from enums.user import UserEnum


class FamousPlace(db.Model):
    __tablename__ = 'famous_place'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    city_id = Column(INTEGER, ForeignKey('city.id'))
    famous_place = Column(String(50), nullable=False)
    entrance_fee = Column(INTEGER, nullable=False)


class City(db.Model):
    __tablename__ = 'city'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    city_name = Column(String(50), nullable=False)
    population = Column(INTEGER, nullable=False)
    country = Column(String(50), nullable=False)


class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    city_id = Column(INTEGER, ForeignKey('city.id'))
    hotel = Column(String(100), nullable=False)
    stars = Column(INTEGER, nullable=False)
    image_link = Column(String(500), nullable=False)
    description = Column(String(500), nullable=False)
    location_link = Column(String(500))  # url
    breakfast_included = Column(Enum(BreakfastEnum))
    transport_from_airport = Column(Enum(TransportEnum))
    # type_of_building = Column()


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


class ApartmentImage(db.Model):
    __tablename__ = 'apartment_id'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    apartment_id = Column(INTEGER, ForeignKey('apartment.id'))
    image = Column(String(750))


class ReserveService(db.Model):
    __tablename__ = 'reserve_service'
    id = Column(INTEGER, primary_key=True, nullable=False)
    reserve_id = Column(INTEGER, ForeignKey('reserve.id'), nullable=False)
    service_id = Column(INTEGER, ForeignKey('service.id'), nullable=False)
    reserve = relationship('Reserve')
    service = relationship('Service')


class Reserve(db.Model):  # many to many with service
    __tablename__ = 'reserve'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    reserve_id = Column(INTEGER, ForeignKey('apartment.id'))
    user_id = Column(INTEGER, ForeignKey('user.id'))
    reserve_start_date = Column(DateTime)
    reserve_finish_date = Column(DateTime)
    reserve_cost = Column(INTEGER, nullable=False)


class Service(db.Model):  # many to many with reserve
    __tablename__ = 'service'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    service = Column(String(150), nullable=False)
    cost = Column(INTEGER, nullable=False)


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


class Review(db.Model):
    __tablename__ = 'review'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    hotel_id = Column(INTEGER, ForeignKey('hotel.id'))
    user_id = Column(INTEGER, ForeignKey('user.id'))
    review = Column(String(500), nullable=True)
    mark = Column(INTEGER, nullable=False)
