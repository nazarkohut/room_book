from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from api.city.schema import city_schema
from api.user.view import auth
from misc.db_misc import session
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
        return jsonify(res), 200


class CityAdd(Resource):
    @jwt_required()
    @auth.login_required
    def post(self):
        try:
            city = request.json
            city_table = City(**city_schema.load(city))
            session.add(city_table)
            session.commit()
            return jsonify(city), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class CityCRUD(Resource):
    @jwt_required()
    @auth.login_required
    def put(self, city_id):
        try:
            city = session.query(City).get(city_id)
            if not city:
                return "Wrong City id", 404

            new_city = City(**city_schema.load(request.json))
            city.city = new_city.city
            city.city_image = new_city.city_image
            city.country = new_city.country
            city.population = new_city.population
            # city.min_cost = new_city.min_cost
            # city.number_of_properties = new_city.number_of_properties
            session.commit()
            return "City info successfully changed ", 200
        except ValidationError as e:
            return e.__dict__.get("messages")

    @jwt_required()
    @auth.login_required
    def delete(self, city_id):
        try:
            city = session.query(City).get(city_id)
            if not city:
                return "City not found", 404
            session.query(City).filter(City.id == city_id).delete()
            session.commit()
            return "City was successfully deleted", 200
        except ValidationError as e:
            return e.__dict__.get("messages")


city_blueprint.add_url_rule('/city', view_func=CityAdd.as_view("CityAdd"))
city_blueprint.add_url_rule('/city/all', view_func=CityBase.as_view("CityBase"))
city_blueprint.add_url_rule('/city/<int:city_id>', view_func=CityCRUD.as_view("CityCRUD"))
