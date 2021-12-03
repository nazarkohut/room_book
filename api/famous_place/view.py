from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from api.famous_place.schema import famous_place_schema
from api.user.view import auth
from misc.db_misc import session
from model.table.city import City
from model.table.famous_place import FamousPlace

famous_place_blueprint = Blueprint("famous_place", __name__)


class FamousPlaceBase(Resource):
    def get(self, city_id):
        famous_place_all = session.query(FamousPlace).filter(FamousPlace.city_id == city_id).all()
        if not famous_place_all:
            return "Not Found", 404
        res = list()
        for famous_place in famous_place_all:
            famous_place = famous_place.__dict__
            del famous_place['_sa_instance_state']
            res.append(famous_place)
        return jsonify(res), 200

    @jwt_required()
    @auth.login_required
    def post(self, city_id):
        try:
            famous_place = request.json
            city_exist = session.query(City).get(city_id)
            if not city_exist:
                return "City with this id does not exist", 404
            famous_place_table = FamousPlace(**famous_place_schema.load(famous_place), city_id=city_id)
            session.add(famous_place_table)
            session.commit()
            return jsonify(famous_place), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class FamousPlaceCRUD(Resource):
    @jwt_required()
    @auth.login_required
    def put(self, famous_place_id):
        try:
            famous_place = session.query(FamousPlace).get(famous_place_id)
            info = request.json
            city_exist = session.query(City).get(info['city_id'])
            if not city_exist:
                return "City with this id does not exist", 404

            if not famous_place:
                return "Famous place with this id doesn't exist", 404

            new_famous_place = FamousPlace(**famous_place_schema.load(request.json))
            famous_place.city_id = new_famous_place.city_id
            famous_place.famous_place = new_famous_place.famous_place
            famous_place.famous_place_image = new_famous_place.famous_place_image
            famous_place.entrance_fee = new_famous_place.entrance_fee
            session.commit()
            return "Famous place info successfully changed", 200
        except ValidationError as e:
            return e.__dict__.get("messages")

    @jwt_required()
    @auth.login_required
    def delete(self, famous_place_id):
        try:
            famous_place = session.query(FamousPlace).get(famous_place_id)
            if not famous_place:
                return "Famous place not found", 404
            session.query(FamousPlace).filter(FamousPlace.id == famous_place_id).delete()
            session.commit()
            return "Famous place was successfully deleted", 200
        except ValidationError as e:
            return e.__dict__.get("messages")


famous_place_blueprint.add_url_rule('/famous_place/<int:city_id>',
                                    view_func=FamousPlaceBase.as_view("FamousPlaceBase"))

famous_place_blueprint.add_url_rule('/particular_famous_place/<int:famous_place_id>',
                                    view_func=FamousPlaceCRUD.as_view("FamousPlaceCRUD"))

