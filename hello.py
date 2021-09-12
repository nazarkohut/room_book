from flask_restful import Resource


class HelloWorld(Resource):
    def get(self, id):
        return {"Hello World": id}
