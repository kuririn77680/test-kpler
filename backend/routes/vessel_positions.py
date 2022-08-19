from flask import Blueprint, jsonify, request, Response
from backend.models.vessel_position import VesselPosition, VesselPositionSchema
from backend.extensions import db
from backend.dto.vessel_position import VesselPositionCreationSchema

vp_bp = Blueprint("vessel_positions", __name__, url_prefix="/vessel_positions")
vessel_position_schema = VesselPositionSchema()
vessel_position_creation_schema = VesselPositionCreationSchema()


@vp_bp.route("", methods=["GET"])
def get_all_vessel_posistion():
    all_vessel_position = VesselPosition.query.all()
    return jsonify(vessel_position_schema.dump(all_vessel_position, many=True)), 200


@vp_bp.route("/<vessel_id>", methods=["GET"])
def get_vessel_posistion(vessel_id):
    vessel_position = VesselPosition.query.filter_by(vessel_id=vessel_id).all()
    return jsonify(vessel_position_schema.dump(vessel_position, many=True))


@vp_bp.route("/add_vessel_position", methods=["POST"])
def add_vessel_position():
    data = request.json
    new_vessel_position = vessel_position_creation_schema.load(data)

    vessel_positions = VesselPosition.query.filter_by(vessel_id=new_vessel_position.vessel_id,
                                                      received_time_utc=new_vessel_position.received_time_utc).all()
    if not vessel_positions:
        db.session.add(new_vessel_position)
        db.session.commit()

        return Response(status=201)

    else:
        return jsonify({"message": "the association vessel_id:received_time_utc already have an entry"})
