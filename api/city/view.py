from flask import Blueprint, request, jsonify
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
        return jsonify(res), 200


class CityAdd(Resource):
    def post(self):
        city = request.json
        city_table = City(**city_schema.load(city))
        session.add(city_table)
        session.commit()
        return jsonify(city), 200


class CityCRUD(Resource):
    def put(self, city_id):
        city = session.query(City).get(city_id)
        if not city:
            return "Wrong City id", 400

        new_city = City(**city_schema.load(request.json))
        city.city = new_city.city
        city.city_image = new_city.city_image
        city.country = new_city.country
        city.population = new_city.population
        # city.min_cost = new_city.min_cost
        # city.number_of_properties = new_city.number_of_properties
        session.commit()
        return "City info successfully changed ", 200

    def delete(self, city_id):
        city = session.query(City).get(city_id)
        if not city:
            return "City not found", 404
        session.query(City).filter(City.id == city_id).delete()
        session.commit()
        return "City was successfully deleted", 200


city_blueprint.add_url_rule('/city', view_func=CityAdd.as_view("CityAdd"))
city_blueprint.add_url_rule('/city/all', view_func=CityBase.as_view("CityBase"))
city_blueprint.add_url_rule('/city/<int:city_id>', view_func=CityCRUD.as_view("CityCRUD"))
