import sqlalchemy.exc
from flask import jsonify, Blueprint, request
from flask_restful import Resource

from api.reserve.schema import reserve_schema
from check_db import session
from model.table.apartment import Apartment
from model.table.reserve import Reserve

reserve_blueprint = Blueprint("reserve", __name__)


class ReserveBase(Resource):
    def get(self, apartment_id):
        reserve_list = session.query(Reserve).filter(Reserve.reserve_id == apartment_id).all()
        if not reserve_list:
            return "It looks like there are no reserves for this apartment", 400
        res = list()
        for reserve in reserve_list:
            reserve = reserve.__dict__
            del reserve['_sa_instance_state']
            res.append(reserve)
        return jsonify(res), 200

    def post(self, apartment_id):
        reserve = request.json
        reserve_table = Reserve(**reserve_schema.load(reserve), reserve_id=apartment_id)
        apartment_exist = session.query(Apartment).filter(Apartment.id == apartment_id).all()
        if not apartment_exist:
            return "You can not relate this reserve to such apartment because it doesn't exist", 404
        session.add(reserve_table)
        session.commit()
        return jsonify(reserve), 200


class ReserveCRUD(Resource):
    def delete(self, reserve_id):
        reserve = session.query(Reserve).get(reserve_id)
        if not reserve:
            return "Reserve doesn't exist", 400
        try:
            session.query(Reserve).filter(Reserve.id == reserve_id).delete()
        except sqlalchemy.exc.IntegrityError:
            return "First you need to delete relation with user or user itself \
            or relation with apartment or apartment itself", 400

        session.commit()
        return "Reserve was successfully deleted", 200


reserve_blueprint.add_url_rule('/reserve/<int:apartment_id>', view_func=ReserveBase.as_view("ReserveBase"))
reserve_blueprint.add_url_rule('/reserve/<int:reserve_id>', view_func=ReserveCRUD.as_view("ReserveCRUD"))
