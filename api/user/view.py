from datetime import datetime, timezone

from flask import Blueprint, request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from passlib.hash import bcrypt
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from api.user.schema import register_schema
from misc.db_misc import session
from model.table.blacklisted_token import TokenBlackList
from model.table.reserve import Reserve
from model.table.user import User
from flask_httpauth import HTTPBasicAuth

user_blueprint = Blueprint('user_blueprint', __name__)
admin_blueprint = Blueprint('admin', __name__)


class RegisterApi(Resource):
    def post(self):
        try:
            user = User(**register_schema.load(request.json))
            if session.query(User).filter(User.email == f'{user.email}').count():
                return "User with this email already registered", 400

            if session.query(User).filter(User.username == f'{user.username}').count():
                return "User with this username already registered", 404

            session.add(user)
            session.commit()
            token = user.get_token()
            return jsonify({'access_token': token}), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class LoginApi(Resource):
    def post(self):
        try:
            user = session.query(User).filter(User.email == request.json['email']).one()
            if not bcrypt.verify(request.json['password'], user.password):
                raise Exception('Wrong user password')
            token = user.get_token()
            return jsonify({'access_token': token}), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class LogoutApi(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()["jti"]
            now = datetime.now(timezone.utc)
            session.add(TokenBlackList(jti=jti, blacklisted_at=now))
            session.commit()
            return jsonify(msg="JWT revoked"), 200
        except ValidationError as e:
            return e.__dict__.get("messages"), 400


class Profile(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            user_info = session.query(User.email, User.username).filter(User.id == user_id).all()
            if not user_info:
                return jsonify({"msg": "User doesn't exist"}), 404
            user_reserves = session.query(Reserve).filter(Reserve.user_id == user_id).all()
            profile = {"email": user_info[0][0], "username": user_info[0][1], "user_reserves": user_reserves}
            return jsonify(profile), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


class ChangeUserPassword(Resource):
    @jwt_required()
    def put(self):
        try:
            user_id = get_jwt_identity()
            old_password = session.query(User.password).filter(User.id == user_id)
            info = request.json

            if not bcrypt.verify(info['old_password'], old_password[0][0]):
                return jsonify({"msg": "old_password is not correct"})
            session.query(User).filter(User.id == user_id).update({"password": str(bcrypt.hash(info['new_password']))})
            session.commit()
            return jsonify({"msg": "Password successfully changed"}), 200
        except ValidationError as e:
            return e.__dict__.get("messages")


# related to registration
user_blueprint.add_url_rule('/registration', view_func=RegisterApi.as_view("register"))
user_blueprint.add_url_rule('/login', view_func=LoginApi.as_view("login"))
user_blueprint.add_url_rule('/logout', view_func=LogoutApi.as_view("logout"))
# related to profile
user_blueprint.add_url_rule('/profile/<int:user_id>', view_func=Profile.as_view('profile'))
user_blueprint.add_url_rule('/profile/change/password', view_func=ChangeUserPassword.as_view('change_user_password'))

# admin verification
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    # if username != request.view_args.get('username'):
    #     return False
    u = session.query(User).filter_by(email=email).first()
    if not u or not bcrypt.verify(password, u.password):
        return False
    if not u.is_admin:
        return False
    return True


