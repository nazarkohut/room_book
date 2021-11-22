from model.setup.sql_imports import *


class City(db.Model):
    __tablename__ = 'city'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    city_image = Column(String(200), nullable=True)
    city = Column(String(50), nullable=False)
    population = Column(INTEGER, nullable=False)
    country = Column(String(50), nullable=False)
