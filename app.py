from flask import Flask
from flask_restful import Api

from hello import HelloWorld

app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True)

api.add_resource(HelloWorld, "/api/v1/hello-world/<int:id>")
