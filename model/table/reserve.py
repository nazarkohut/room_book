from model.setup.sql_imports import *
from model.table.user import User
from model.table.apartment import Apartment
# from model.table.reserve_service import ReserveService


class Reserve(db.Model):  # many to many with service
    __tablename__ = 'reserve'
    id = Column(INTEGER, primary_key=True, unique=True, nullable=False)
    reserve_id = Column(INTEGER, ForeignKey('apartment.id'))
    user_id = Column(INTEGER, ForeignKey('user.id'))
    reserve_start_date = Column(DateTime)
    reserve_finish_date = Column(DateTime)
    reserve_cost = Column(INTEGER, nullable=False)

