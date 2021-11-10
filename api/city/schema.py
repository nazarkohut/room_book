from marshmallow import Schema, fields


class CitySchema(Schema):
    city = fields.Str()
    city_image = fields.Str(unique=True)
    country = fields.Str()
    population = fields.Integer()
    # min_cost = fields.Integer()
    # number_of_properties = fields.Integer()

    class Meta:
        fields = (
            'city',
            'city_image',
            'country',
            'population',
            # 'min_cost',
            # 'number_of_properties'
        )


city_schema = CitySchema()
