import sqlalchemy.exc
from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.hotel.schema import hotel_schema
from misc.db_misc import session
from model.table.city import City
from model.table.hotel import Hotel

hotel_blueprint = Blueprint("hotel", __name__)


class HotelBase(Resource):
    def get(self, city_id):
        cities = session.query(Hotel).filter(Hotel.city_id == city_id).all()
        if not cities:
            return "It look like there are no hotels in this city", 404

        res = list()
        for city in cities:
            city = city.__dict__
            del city['_sa_instance_state']
            res.append(city)
        return jsonify(res), 200


class HotelAdd(Resource):
    @jwt_required()
    def post(self, city_id):
        hotel = request.json
        hotel_table = Hotel(**hotel_schema.load(hotel), city_id=city_id)
        city_exist = session.query(City).filter(City.id == city_id).all()

        if not city_exist:
            return "Looks like there is no such City", 404

        session.add(hotel_table)
        session.commit()
        return jsonify(hotel), 200


class HotelCRUD(Resource):
    def get(self, hotel_id):
        hotel = session.query(Hotel).get(hotel_id)
        if not hotel:
            return "It looks like there is no such hotel", 404

        hotel = hotel.__dict__
        del hotel['_sa_instance_state']
        return jsonify(hotel), 200

    @jwt_required()
    def put(self, hotel_id):
        hotel = session.query(Hotel).get(hotel_id)

        if not hotel:
            return "Looks like there is no such hotel", 404

        info = request.json
        city_exist = session.query(City).get(info['city_id'])

        if not city_exist:
            return "City with this id does not exist", 400

        new_hotel = Hotel(**hotel_schema.load(info))
        hotel.city_id = new_hotel.city_id
        hotel.hotel = new_hotel.hotel
        hotel.stars = new_hotel.stars
        hotel.image_link = new_hotel.image_link
        hotel.description = new_hotel.description

        # hotel.location_on_map = new_hotel.location_on_map
        # hotel.breakfast_included = new_hotel.location_on_map.breakfast_included

        hotel.transport_from_airport = new_hotel.transport_from_airport

        hotel = hotel.__dict__
        del hotel['_sa_instance_state']
        return jsonify(hotel), 200

    @jwt_required()
    def delete(self, hotel_id):
        hotel = session.query(Hotel).get(hotel_id)
        if not hotel:
            return "Hotel doesn't exist", 404
        try:
            session.query(Hotel).filter(Hotel.id == hotel_id).delete()
        except sqlalchemy.exc.IntegrityError:
            return "First you need to delete relation with city or city itself", 400

        session.commit()
        return "Hotel was successfully deleted", 200


hotel_blueprint.add_url_rule('/hotels/<int:city_id>', view_func=HotelBase.as_view("HotelBase"))
hotel_blueprint.add_url_rule('/hotel/<int:city_id>', view_func=HotelAdd.as_view("HotelAdd"))
hotel_blueprint.add_url_rule('/hotel/<int:hotel_id>', view_func=HotelCRUD.as_view("HotelCRUD"))

