from flask import Blueprint, request, jsonify
from flask_restful import Resource

from api.famous_place.schema import famous_place_schema
from check_db import session
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

    def post(self, city_id):
        famous_place = request.json
        famous_place_table = FamousPlace(**famous_place_schema.load(famous_place), city_id=city_id)
        session.add(famous_place_table)
        session.commit()
        return jsonify(famous_place), 200


class FamousPlaceCRUD(Resource):
    # def get(self, famous_place_id):
    #     famous_place = session.query(FamousPlace).get(famous_place_id)
    #     if not famous_place:
    #         return "Famous place with this id doesn't exist", 404
    #     famous_place = famous_place.__dict__
    #     del famous_place['_sa_instance_state']
    #     return jsonify(famous_place), 200

    def put(self, famous_place_id):
        famous_place = session.query(FamousPlace).get(famous_place_id)
        if not famous_place:
            return "Famous place with this id doesn't exist", 400

        new_famous_place = FamousPlace(**famous_place_schema.load(request.json))
        famous_place.city_id = new_famous_place.city_id
        famous_place.famous_place = new_famous_place.famous_place
        # new_famous_place.famous_place_image = famous_place.famous_place_image
        famous_place.entrance_fee = new_famous_place.entrance_fee
        session.commit()
        return "Famous place info successfully changed", 200

    def delete(self, famous_place_id):
        famous_place = session.query(FamousPlace).get(famous_place_id)
        if not famous_place:
            return "Wrong famous place id", 400
        session.query(FamousPlace).filter(FamousPlace.id == famous_place_id).delete()
        session.commit()
        return "Famous place was successfully deleted", 200


famous_place_blueprint.add_url_rule('/famous_place/<int:city_id>',
                                    view_func=FamousPlaceBase.as_view("FamousPlaceBase"))

famous_place_blueprint.add_url_rule('/particular_famous_place/<int:famous_place_id>',
                                    view_func=FamousPlaceCRUD.as_view("FamousPlaceCRUD"))

