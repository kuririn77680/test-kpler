import csv
from backend import create_app
from flask import request, jsonify, Response
import os
from werkzeug.utils import secure_filename
from backend.extensions import db
from backend.routes.vessel_positions import VesselPositionCreationSchema
from backend.models.vessel_position import VesselPosition

app = create_app()

upload_dir = os.path.join(app.instance_path, 'upload')
vessel_position_creation_schema = VesselPositionCreationSchema()


@app.route("/upload_vessel_position_csv", methods=["POST"])
def upload_file():
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
                else:
                    existing_entry.append(line)

            except:
                failed_line.append(line)

            line += 1

        db.session.commit()
        file.close()
        os.remove(upload_dir + "/" + secure_filename(filename))

    if len(failed_line) > 0 and len(existing_entry):
        message = "error format data on line: " + str(failed_line) + "\n " \
                    "error already existing entry on line " + str(existing_entry)
        return jsonify({"message": message}), 201

    elif len(existing_entry) > 0:
        message = "error already existing entry on line " + str(existing_entry)
        return jsonify({"message": message}), 201

    elif len(failed_line) > 0:
        message = "error format data on line: " + str(failed_line)
        return jsonify({"message": message}), 201

    else:
        return Response(status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
