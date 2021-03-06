from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import username, password, server, Config

app = Flask(__name__)
api = Api(app)

jwt = JWTManager(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{username}:{password}@{server}/room_book_db"

migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)

from api.hotel.view import hotel_blueprint
from api.city.view import city_blueprint
from api.apartment.view import apartment_blueprint
from api.famous_place.view import famous_place_blueprint
from api.reserve.view import reserve_blueprint
from api.user.view import user_blueprint, admin_blueprint

app.register_blueprint(city_blueprint)
app.register_blueprint(apartment_blueprint)
app.register_blueprint(famous_place_blueprint)
app.register_blueprint(hotel_blueprint)
app.register_blueprint(reserve_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(admin_blueprint)
