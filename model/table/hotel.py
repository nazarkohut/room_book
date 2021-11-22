from model.setup.sql_imports import *
from enums.hotel import BreakfastEnum, TransportEnum
from model.table.city import City


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
