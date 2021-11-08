from flask import Blueprint, request, jsonify
from flask_restful import Resource

from api.famous_place.schema import famous_place_schema
from check_db import session
from model.table.city import City
from model.table.famous_place import FamousPlace

famous_place_blueprint = Blueprint("famous_place", __name__)


class FamousPlaceBase(Resource):
    def get(self, city_id):
        famous_place_all = session.query(FamousPlace).filter(City.id == city_id).all()
        if not famous_place_all:
            return "Not Found", 404
        res = list()
        for famous_place in famous_place_all:
            famous_place = famous_place.__dict__
            del famous_place['_sa_instance_state']
            res.append(famous_place)
        return jsonify(res), 200

    def post(self):
        pass


class FamousPlaceCRUD(Resource):
    def get(self, famous_place_id):
        famous_place = session.query(FamousPlace).get(famous_place_id).__dict__
        del famous_place['_sa_instance_state']
        return jsonify(famous_place), 200

    def put(self, famous_place_id):
        famous_place = session.query(FamousPlace).get(famous_place_id)
        if not famous_place:
            return "Wrong famous place id", 400

        new_famous_place = FamousPlace(**famous_place_schema.load(request.json))
        new_famous_place.city_id = famous_place.city_id
        new_famous_place.famous_place = famous_place.famous_place
        # new_famous_place.famous_place_image = famous_place.famous_place_image
        new_famous_place.entrance_fee = famous_place.entrance_fee
        session.commit()
        return "Famous place info successfully changed", 200

    def delete(self, famous_place_id):
        famous_place = session.query(FamousPlace).get(famous_place_id)
        if not famous_place:
            return "Wrong famous place id", 400
        session.query(FamousPlace).filter(famous_place_id).delete()
        session.commit()
        return "Famous place was successfully deleted", 200


famous_place_blueprint.add_url_rule('/famous_place/<int:city_id>',
                                    view_func=FamousPlaceBase.as_view("FamousPlaceBase"))

famous_place_blueprint.add_url_rule('/particular_famous_place/<int:famous_place_id>',
                                    view_func=FamousPlaceCRUD.as_view("FamousPlaceCRUD"))

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
