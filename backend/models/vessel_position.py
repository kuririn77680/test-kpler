from backend.extensions import db


class VesselPosition(db.Model):
    __tablename__ = "vessel_position"

    id = db.Column(db.Integer, primary_key=True)
    vessel_id = db.Column(db.Integer, nullable=False)
    received_time_utc = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)