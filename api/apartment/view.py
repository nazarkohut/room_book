from http import HTTPStatus

from flask import Blueprint, request, Response, jsonify
from flask_restful import Resource

from api.apartment.schema import apartment_schema
from check_db import session
from model.table.apartment import Apartment

apartment_blueprint = Blueprint("apartment", __name__)


class ApartmentBase(Resource):
    def get(self, hotel_id):
        apartment_list = session.query(Apartment).filter(Apartment.hotel_id == hotel_id).all()
        res = list()
        for apartment in apartment_list:
            apartment = apartment.__dict__
            del apartment['_sa_instance_state']
            res.append(apartment)
        if not res:
            return Response("Not Found", status=HTTPStatus.NOT_FOUND)
        return str(res)

    def post(self, hotel_id):
        apartment = request.json
        apartment_table = Apartment(**apartment_schema.load(apartment), hotel_id=hotel_id)  ####
        session.add(apartment_table)
        session.commit()
        return jsonify(apartment), 200


class ApartmentCRUD(Resource):
    def get(self, apartment_id):
        character = session.query(Apartment).get(apartment_id).__dict__
        del character['_sa_instance_state']
        return str(character), 200

    def put(self, apartment_id):
        apartment = session.query(Apartment).get(apartment_id)
        if not apartment:
            return "Wrong Character id", 400

        new_apartment = Apartment(**apartment_schema.load(request.json))

        apartment.apartment_id = new_apartment.apartment_id
        apartment.image = new_apartment.image
        apartment.is_available = new_apartment.is_available
        apartment.room_capacity = new_apartment.room_capacity
        apartment.floor = new_apartment.floor
        apartment.cost = new_apartment.cost
        apartment.description = apartment.description
        session.commit()
        return "Apartment info successfully changed ", 200

    def delete(self, apartment_id):
        apartment = session.query(Apartment).get(apartment_id)
        if not apartment:
            return "Wrong Apartment id", 400
        session.query(Apartment).filter(Apartment.id == apartment_id).delete()
        session.commit()
        return "Apartment was successfully deleted", 200


apartment_blueprint.add_url_rule('/apartment/<int:hotel_id>', view_func=ApartmentBase.as_view("ApartmentBase"))
apartment_blueprint.add_url_rule('/particular_apartment/<int:apartment_id>',
                                 view_func=ApartmentCRUD.as_view("ApartmentCRUD"))
