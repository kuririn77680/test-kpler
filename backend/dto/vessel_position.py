from marshmallow import fields, Schema, validates, ValidationError, post_load
from backend.models.vessel_position import VesselPosition


class VesselPositionCreationSchema(Schema):
    vessel_id = fields.Integer(required=True)
    received_time_utc = fields.DateTime(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    @validates("latitude")
    @validates("longitude")
    def validate_coordinate(self, value):
        if value <= -180.00 or value >= 180.00:
            raise ValidationError("Latitude or longitude must be defined between -180.00 and +180.00")


    @post_load
    def make_vaseel_position(self, data, **kwargs):
        return VesselPosition(**data)