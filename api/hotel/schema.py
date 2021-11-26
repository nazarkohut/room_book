from marshmallow import fields, Schema, EXCLUDE


class HotelSchema(Schema):
    city_id = fields.Int()
    hotel = fields.Str()
    stars = fields.Int()
    image_link = fields.Str()
    description = fields.Str()
    #location_link = fields.Str()
    # breakfast_included = fields.Str()
    # transport_from_airport = fields.

    class Meta:
        fields = (
            "city_id",
            "hotel",
            "stars",
            "image_link",
            "description",
            #"location_link"
            # "breakfast_included",
            #"transport_from_airport",
        )
        # unknown = EXCLUDE


hotel_schema = HotelSchema()
