from flask import Blueprint, jsonify, request, Response
from backend.models.vessel_position import VesselPosition
from backend.extensions import db

vp_bp = Blueprint("vessel_positions", __name__, url_prefix="/vessel_positions")


@vp_bp.route("/all_vessel_position", methods=["GET"])
def get_all_vessel_posistion():
    all_vessel_position = VesselPosition.query.all()
    return jsonify([{"vessel_id": vp.vessel_id, "received_time_utc": vp.received_time_utc, "latitude": vp.latitude,
                     "longitude": vp.longitude} for vp in all_vessel_position])


@vp_bp.route("/<vessel_id>", methods=["GET"])
def get_vessel_posistion(vessel_id):
    vessel_position = VesselPosition.query.filter_by(vessel_id=vessel_id)
    return jsonify([{"vessel_id": vp.vessel_id, "received_time_utc": vp.received_time_utc, "latitude": vp.latitude,
                     "longitude": vp.longitude} for vp in vessel_position])


@vp_bp.route("/add_vessel_position", methods=["POST"])
def add_vessel_position():
    data = request.json
    print(data)

    vessel_position = VesselPosition()
    vessel_position.vessel_id = data["vessel_id"]
    vessel_position.received_time_utc = data["received_time_utc"]
    vessel_position.latitude = data["latitude"]
    vessel_position.longitude = data["longitude"]

    db.session.add(vessel_position)
    db.session.commit()
    return Response(status=204)


@vp_bp.route("/add_vessel_position_csv", methods=["POST"])
def add_vessel_position_csv():
    # file = request.files
    # read csv file line per line validate, add content
    return Response(status=204)
