from model.setup.sql_imports import *
from model.table.city import City


class FamousPlace(db.Model):
    __tablename__ = 'famous_place'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    city_id = Column(INTEGER, ForeignKey('city.id'))
    famous_place = Column(String(50), nullable=False)
    entrance_fee = Column(INTEGER, nullable=False)
    famous_place_image = Column(String(100), nullable=True)
