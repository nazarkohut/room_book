from model.setup.sql_imports import *
from model.table.apartment import Apartment


class ApartmentImage(db.Model):
    __tablename__ = 'apartment_id'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    apartment_id = Column(INTEGER, ForeignKey('apartment.id'))
    image = Column(String(750))
