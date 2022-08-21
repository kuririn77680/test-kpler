from marshmallow import fields, Schema, validates, ValidationError, post_load, validates_schema
from backend.models.vessel_position import VesselPosition
from global_land_mask import globe


class VesselPositionCreationSchema(Schema):
    vessel_id = fields.Integer(required=True)
    received_time_utc = fields.DateTime(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

    @validates("latitude")
    def validate_latitude(self, value):
        if value <= -90.00 or value >= 90.00:
            raise ValidationError("Latitude must be defined between -90.00 and +90.00")

    @validates("longitude")
    def validate_longitude(self, value):
        if value <= -180.00 or value >= 180.00:
            raise ValidationError("longitude must be defined between -180.00 and +180.00")

    @validates_schema()
    def validate_vessel_position(self, data, **kwargs):
        is_in_ocean = globe.is_ocean(data["latitude"], data["longitude"])
        if not is_in_ocean:
            raise ValidationError("Vessel must be declared on sea")

    @post_load
    def make_vassel_position(self, data, **kwargs):
        return VesselPosition(**data)
