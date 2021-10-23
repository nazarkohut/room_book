from model.setup.sql_imports import *


class ReserveService(db.Model):
    __tablename__ = 'reserve_service'
    id = Column(INTEGER, primary_key=True, nullable=False)
    reserve_id = Column(INTEGER, ForeignKey('reserve.id'), nullable=False)
    service_id = Column(INTEGER, ForeignKey('service.id'), nullable=False)
    reserve = relationship('Reserve')
    service = relationship('Service')
