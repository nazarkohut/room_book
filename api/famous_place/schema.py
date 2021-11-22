from marshmallow import Schema, fields


class FamousPlaceSchema(Schema):
    city_id = fields.Integer(),
    famous_place = fields.Str(),
    famous_place_image = fields.Str(),
    entrance_fee = fields.Integer()

    class Meta:
        fields = (
            "city_id",
            "famous_place",
            "famous_place_image",
            "entrance_fee"
        )


famous_place_schema = FamousPlaceSchema()
