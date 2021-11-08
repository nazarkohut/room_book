# This file is temporary, it is created in order to check all connections
from datetime import date

from flask_restful import Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app import db
from config import username, password, server
from model.table.apartment import Apartment
from model.table.apartment_image import ApartmentImage
from model.table.city import City
from model.table.famous_place import FamousPlace
from model.table.hotel import Hotel
from model.table.reserve import Reserve
from model.table.reserve_service import ReserveService
from model.table.review import Review
from model.table.service import Service
from model.table.user import User

engine = create_engine(f"mysql+pymysql://root:root@127.0.0.1:3306/room_book_db")
session = Session(bind=engine)


class AddAllTables(Resource):
    def post(self):
        user = User(email='sds3', username='sdfs3', password='dfg3s', birthday=date.today(), is_admin=False,
                    is_bot=False, location_link="link3")

        user1 = User(email='sadsadsa', username='adasdsaddsa', password='dfgdasdsadsad3s', birthday=date.today(), is_admin=False,
                    is_bot=False, location_link="link3")



        reserve = Reserve(
            # reserve_id=1,
            user_id=1,
            reserve_start_date=date.today(),
            reserve_finish_date=date.today(),
            reserve_cost=500)
        service1 = Service(
            service='service',
            cost=100,
        )
        reserve2 = Reserve(
            # reserve_id=1,
            user_id=1,
            reserve_start_date=date.today(),
            reserve_finish_date=date.today(),
            reserve_cost=500)
        service1 = Service(
            service='service',
            cost=100,
        )
        reserve3 = Reserve(
            # reserve_id=1,
            user_id=2,
            reserve_start_date=date.today(),
            reserve_finish_date=date.today(),
            reserve_cost=500)
        service1 = Service(
            service='service',
            cost=100,
        )

        hotel = Hotel(hotel="Redisson", stars=5, image_link="link", description="description",
                      location_link="link",
                      breakfast_included="all_inclusive",
                      transport_from_airport="car")

        city = City(city_name="Konoha", population=99999, country="Land of Fire")

        famous_place = FamousPlace(
            famous_place='Famous',
            entrance_fee=500)
        review = Review(review='review',
                        mark=5)
        apartment_image = ApartmentImage(image='sdgfsdf')
        rs = ReserveService(reserve_id=1, service_id=1)
        # db.session.add(user)
        # db.session.add(user1)
        # db.session.add(city)
        # db.session.add(hotel)
        # db.session.add(famous_place)
        # db.session.add(review)
        # db.session.add(apartment_image)
        #
        # service1 = Service(service='service', cost=100)
        # db.session.add(service1)

        apartment = Apartment(hotel_id=1, image="", room_capacity=100, floor=1, cost=300, description="asdsadads")
        # db.session.add(reserve)
        # db.session.add(reserve2)
        # db.session.add(reserve3)
        #
        db.session.add(rs)
        db.session.add(apartment)

        db.session.commit()
        db.session.close()
