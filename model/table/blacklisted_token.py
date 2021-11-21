from model.setup.sql_imports import *


class TokenBlackList(db.Model):
    __tablename__ = 'token_black_list'
    id = Column(INTEGER(), primary_key=True)
    jti = Column(String(36), nullable=False)
    blacklisted_at = Column(DateTime(), nullable=False)
