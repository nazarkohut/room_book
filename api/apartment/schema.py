from marshmallow import Schema, fields


class ApartmentSchema(Schema):
    apartment_id = fields.Int(required=False)
    image = fields.Str()
    is_available = fields.Boolean()
    room_capacity = fields.Int(required=True)
    floor = fields.Int(required=True)
    cost = fields.Int(required=True)
    description = fields.Str()

    class Meta:
        fields = ('image', 'is_available', 'room_capacity', 'floor',  'cost', 'description')

apartment_schema = ApartmentSchema()
