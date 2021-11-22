from marshmallow import Schema, fields


class ReserveSchema(Schema):
    reserve_start_date = fields.Date()
    reserve_finish_date = fields.Date()

    class Meta:
        fields = (
            "reserve_start_date",
            "reserve_finish_date"
        )


reserve_schema = ReserveSchema()
