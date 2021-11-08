from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import username, password, server

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://root:root@127.0.0.1:3306/room_book_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)

from check_db import AddAllTables

api.add_resource(AddAllTables, "/api/v1/hello-world/")
