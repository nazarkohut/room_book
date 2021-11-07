# This file is temporary, it is created in order to check all connections
from flask_restful import Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import db
from config import username, password, server
from model.table.apartment_image import ApartmentImage
from model.table.famous_place import FamousPlace
from model.table.hotel import Hotel
from model.table.review import Review

engine = create_engine(f"mysql://{username}:{password}@{server}/room_book_db")
session = Session(bind=engine)


class AddAllTables(Resource):
    def post(self):
        # user = User(email='sds3', username='sdfs3', password='dfg3s', birthday=date.today(), is_admin=False,
        #             is_bot=False, location_link="link3")
        # reserve = Reserve(
        #     # reserve_id=1,
        #     user_id=1,
        #     reserve_start_date=date.today(),
        #     reserve_finish_date=date.today(),
        #     reserve_cost=500)
        # service1 = Service(
        #     service='service',
        #     cost=100,
        # )

        # db.session.add(reserve)
        famous_place = FamousPlace(
            famous_place='Famous',
            entrance_fee=500)
        review = Review(review='review',
                        mark=5)
        apartment_image = ApartmentImage(image='sdgfsdf')
        hotel = Hotel(hotel="Redisson", stars=5, image_link="link", description="description",
                      location_link="link",
                      breakfast_included="all_inclusive",
                      transport_from_airport="car")
        db.session.add(hotel)
        db.session.commit()
