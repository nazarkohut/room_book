from http import HTTPStatus

from flask import Blueprint, request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from api.apartment.schema import apartment_schema
from misc.db_misc import session
from misc.permissions import is_hotel_owner
from model.table.apartment import Apartment
from model.table.hotel import Hotel
from model.table.user import User

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

    @jwt_required()
    def post(self, hotel_id):
        try:
            user_id = get_jwt_identity()
            if not is_hotel_owner(user_id):
                return jsonify({"msg": "Permission  denied"}), 403

            apartment = request.json
            apartment_table = Apartment(**apartment_schema.load(apartment), hotel_id=hotel_id)
            hotel_exist = session.query(Hotel).get(hotel_id)
            if not hotel_exist:
                return "Hotel does not exist", 404
            session.add(apartment_table)
            session.commit()
            return jsonify(apartment), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class ApartmentCRUD(Resource):
    def get(self, apartment_id):
        character = session.query(Apartment).get(apartment_id)
        if not character:
            return "Apartment doesn't exist", 404
        character = character.__dict__
        del character['_sa_instance_state']
        return str(character), 200

    @jwt_required()
    def put(self, apartment_id):
        try:
            user_id = get_jwt_identity()
            if not is_hotel_owner(user_id):
                return jsonify({"msg": "Permission  denied"}), 403

            apartment = session.query(Apartment).get(apartment_id)
            if not apartment:
                return "Wrong Character id", 400

            new_apartment = Apartment(**apartment_schema.load(request.json))

            #apartment.apartment_id = new_apartment.apartment_id
            apartment.image = new_apartment.image
            apartment.is_available = new_apartment.is_available
            apartment.room_capacity = new_apartment.room_capacity
            apartment.floor = new_apartment.floor
            apartment.cost = new_apartment.cost
            apartment.description = apartment.description
            session.commit()
            return "Apartment info successfully changed ", 200
        except ValidationError as e:
            return e.__dict__.get("messages")

    @jwt_required()
    def delete(self, apartment_id):
        try:
            user_id = get_jwt_identity()
            user = session.query(User).filter(User.id == user_id).first()

            if not (is_hotel_owner(user_id) or user.is_admin):
                return jsonify({"msg": "Permission  denied"}), 403

            apartment = session.query(Apartment).get(apartment_id)
            if not apartment:
                return "Wrong Apartment id", 400
            session.query(Apartment).filter(Apartment.id == apartment_id).delete()
            session.commit()
            return "Apartment was successfully deleted", 200
        except ValidationError as e:
            return e.__dict__.get("messages")


apartment_blueprint.add_url_rule('/apartment/<int:hotel_id>', view_func=ApartmentBase.as_view("ApartmentBase"))
apartment_blueprint.add_url_rule('/particular_apartment/<int:apartment_id>',
                                 view_func=ApartmentCRUD.as_view("ApartmentCRUD"))
