from flask import jsonify
from flask_restful import Resource

from check_db import session
from model.table.hotel import Hotel


class HotelBase(Resource):
    def get(self, city_id):
        city = session.query(Hotel).filter(Hotel.city_id == city_id).all()
        if not city:
            return "It look like there are no hotels in this city", 404
        return jsonify(city)

