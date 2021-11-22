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


from check_db import AddAllTables
api.add_resource(AddAllTables, "/api/v1/hello-world/")
