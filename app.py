from flask import Flask
from flask_restful import Api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from config import username, password, server


app = Flask(__name__)
api = Api(app)


db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{username}:{password}@{server}/room_book_db"
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)


from api.city.view import city_blueprint
from api.apartment.view import apartment_blueprint

app.register_blueprint(city_blueprint)
app.register_blueprint(apartment_blueprint)
