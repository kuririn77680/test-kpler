import csv
import os

from flask import Blueprint, jsonify, request, Response, app
from backend.models.vessel_position import VesselPosition, VesselPositionSchema
from backend.extensions import db
from backend.dto.vessel_position import VesselPositionCreationSchema
from werkzeug.utils import secure_filename

vp_bp = Blueprint("vessel_positions", __name__, url_prefix="/vessel_positions")
vessel_position_schema = VesselPositionSchema()
vessel_position_creation_schema = VesselPositionCreationSchema()

dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
upload_dir = os.path.join(dirname, 'instance/upload')


@vp_bp.route("", methods=["GET"])
def get_all_vessel_position():
    all_vessel_position = VesselPosition.query.all()
    return jsonify(vessel_position_schema.dump(all_vessel_position, many=True)), 200


@vp_bp.route("/<vessel_id>", methods=["GET"])
def get_vessel_position(vessel_id):
    vessel_position = VesselPosition.query.filter_by(vessel_id=vessel_id).all()
    return jsonify(vessel_position_schema.dump(vessel_position, many=True)), 200


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
        return jsonify({"message": "the association vessel_id:received_time_utc already have an entry"}), 400


@vp_bp.route("/upload_vessel_position_csv", methods=["POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["csvfile"]
        filename = file.filename
        file.save(os.path.join(upload_dir, secure_filename(filename)))

        file = open(os.path.join(upload_dir, secure_filename(filename)), "r")
        csvreader = csv.reader(file)
        header = next(csvreader)
        line = 2
        failed_line = []
        existing_entry = []
        valid = []
        for row in csvreader:
            try:
                data = {"vessel_id": row[0],
                        "received_time_utc": row[1],
                        "latitude": row[2],
                        "longitude": row[3]}
                new_vessel_position = vessel_position_creation_schema.load(data)

                vessel_positions = VesselPosition.query.filter_by(vessel_id=new_vessel_position.vessel_id,
                                                                  received_time_utc=new_vessel_position.received_time_utc).all()

                if not vessel_positions:
                    db.session.add(new_vessel_position)
                    valid.append(line)
                else:
                    existing_entry.append(line)

            except:
                failed_line.append(line)

            line += 1

        db.session.commit()
        file.close()
        os.remove(upload_dir + "/" + secure_filename(filename))

    if len(valid) <= 0:
        message = "no data inserted from upoladed file"
        return jsonify({"message": message}), 200

    elif len(failed_line) > 0 and len(existing_entry):
        message = "error format data on line: " + str(failed_line) + "\n " \
                                                                     "error already existing entry on line " + str(
            existing_entry)
        return jsonify({"message": message}), 201

    elif len(existing_entry) > 0:
        message = "error already existing entry on line " + str(existing_entry)
        return jsonify({"message": message}), 201

    elif len(failed_line) > 0:
        message = "error format data on line: " + str(failed_line)
        return jsonify({"message": message}), 201


    else:
        return Response(status=201)
