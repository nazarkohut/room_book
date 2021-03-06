import sqlalchemy.exc
from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError

from api.reserve.schema import reserve_schema
from misc.db_misc import session
from misc.permissions import is_hotel_owner
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

    @jwt_required()
    def post(self, apartment_id):
        try:
            user_id = get_jwt_identity()
            if is_hotel_owner(user_id):
                return jsonify({"msg": "Permission  denied"}), 403

            reserve = request.json
            if reserve['reserve_start_date'] > reserve['reserve_finish_date']:
                return "Sorry provide valid dates for reserve", 400

            apartment_exist = session.query(Apartment).filter(Apartment.id == apartment_id).all()
            if not apartment_exist:
                return "You can not relate this reserve to such apartment because it doesn't exist", 404
            reserve_table = Reserve(**reserve_schema.load(reserve), reserve_id=apartment_id)
            session.add(reserve_table)
            session.commit()
            return jsonify(reserve), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class ReserveCRUD(Resource):
    @jwt_required()
    def delete(self, reserve_id):
        try:
            user_id = get_jwt_identity()
            if is_hotel_owner(user_id):
                return jsonify({"msg": "Permission  denied"}), 403

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
        except ValidationError as e:
            return e.__dict__.get("messages")


reserve_blueprint.add_url_rule('/reserve/<int:apartment_id>', view_func=ReserveBase.as_view("ReserveBase"))
reserve_blueprint.add_url_rule('/reserve/<int:reserve_id>', view_func=ReserveCRUD.as_view("ReserveCRUD"))
