

from flask import Blueprint, request
from flask_restful import Resource

from api.city.schema import city_schema
from check_db import session
from model.table.city import City

city_blueprint = Blueprint("city", __name__)


class CityBase(Resource):
    def get(self):
        all_cities = session.query(City).all()
        if not all_cities:
            return "Not Found", 404
        res = list()
        for city in all_cities:
            city = city.__dict__
            del city['_sa_instance_state']
            res.append(city)
        return str(res), 200

    def post(self):
        pass


class CityCRUD(Resource):
    def get(self):
        pass

    def put(self, city_id):
        city = session.query(City).get(city_id)
        if not city:
            return "Wrong City id", 400

        new_city = City(**city_schema.load(request.json))
        city.city = new_city.city
        city.city_image = new_city.city_image
        city.country = new_city.country
        city.population = new_city.population
        city.min_cost = new_city.min_cost
        city.number_of_properties = new_city.number_of_properties
        session.commit()
        return "City info successfully changed ", 200

    def delete(self, city_id):
        city = session.query(City).get(city_id)
        if not city:
            return "Wrong City id", 400
        session.query(City).filter(City.id == city_id).delete()
        session.commit()
        return "City was successfully deleted", 200


city_blueprint.add_url_rule('/city/all', view_func=CityBase.as_view("CityBase"))
city_blueprint.add_url_rule('/city/<int:city_id>', view_func=CityCRUD.as_view("CityCRUD"))

# class ApartmentBase(Resource):
#     def get(self, hotel_id):
#         apartment_list = session.query(Apartment).filter(Apartment.hotel_id == hotel_id).all()
#         res = list()
#         for apartment in apartment_list:
#             apartment = apartment.__dict__
#             del apartment['_sa_instance_state']
#             res.append(apartment)
#         if not res:
#             return Response("Not Found", status=HTTPStatus.NOT_FOUND)
#         return str(res)
#
#     def post(self, hotel_id):
#         apartment = request.json
#         apartment_table = Apartment(**apartment_schema.load(apartment))  ####
#         session.add(apartment_table)
#         session.commit()
#         return Response(apartment, status=HTTPStatus.OK)
#
#
# class ApartmentCRUD(Resource):
#     def get(self, apartment_id):
#         character = session.query(Apartment).get(apartment_id).__dict__
#         del character['_sa_instance_state']
#         return str(character), 200
#
#     def put(self, apartment_id):
#         apartment = session.query(Apartment).get(apartment_id)
#         if not apartment:
#             return "Wrong Character id", 400
#
#         new_apartment = Apartment(**apartment_schema.load(request.json))
#
#         apartment.apartment_id = new_apartment.apartment_id
#         apartment.image = new_apartment.image
#         apartment.is_available = new_apartment.is_available
#         apartment.room_capacity = new_apartment.room_capacity
#         apartment.floor = new_apartment.floor
#         apartment.cost = new_apartment.cost
#         apartment.description = apartment.description
#         session.commit()
#         return "Apartment info successfully changed ", 200
#
#     def delete(self, apartment_id):
#         apartment = session.query(Apartment).get(apartment_id)
#         if not apartment:
#             return "Wrong Apartment id", 400
#         session.query(Apartment).filter(Apartment.id == apartment_id).delete()
#         session.commit()
#         return "Apartment was successfully deleted", 200
#
#
# apartment_blueprint.add_url_rule('/apartment/<int:hotel_id>', view_func=ApartmentBase.as_view("ApartmentBase"))
# apartment_blueprint.add_url_rule('/particular_apartment/<int:apartment_id>', view_func=ApartmentCRUD.as_view("ApartmentCRUD"))
