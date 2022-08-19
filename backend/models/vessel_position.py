from backend.extensions import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field


class VesselPosition(db.Model):
    __tablename__ = "vessel_position"

    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column(db.Integer, nullable=False)
    received_time_utc = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float(24), nullable=False)
    longitude = db.Column(db.Float(24), nullable=False)

    def __init__(self, vessel_id, received_time_utc, latitude, longitude):
        self.vessel_id = vessel_id
        self.received_time_utc = received_time_utc
        self.latitude = latitude
        self.longitude = longitude


class VesselPositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VesselPosition
        load_instance = True

    id = auto_field()
    vessel_id = auto_field()
    received_time_utc = auto_field()
    latitude = auto_field()
    longitude = auto_field()