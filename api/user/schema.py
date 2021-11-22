from marshmallow import Schema, fields
from marshmallow.validate import Length


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True, validate=Length(min=10))
    password = fields.Str(required=True)
    birthday = fields.Date(required=True)
    hotel_owner = fields.Boolean(required=True)

    class Meta:
        fields = ('username', 'email', 'birthday', 'hotel_owner', 'password')


register_schema = RegisterSchema()
