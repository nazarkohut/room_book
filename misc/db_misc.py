# This file is temporary, it is created in order to check all connections
from flask_restful import Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import db, jwt
from config import username, password, server
from model.table.apartment_image import ApartmentImage
from model.table.blacklisted_token import TokenBlackList
from model.table.famous_place import FamousPlace
from model.table.hotel import Hotel
from model.table.review import Review

engine = create_engine(f"mysql://{username}:{password}@{server}/room_book_db")
session = Session(bind=engine)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    session.commit()
    token = session.query(TokenBlackList.id).filter_by(jti=jti).scalar()
    return token is not None
