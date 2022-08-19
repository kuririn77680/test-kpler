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
        file.save(os.path.join(upload_dir, secure_filename(file.filename)))

        file = open(os.path.join(upload_dir, secure_filename(file.filename)), "r")
        csvreader = csv.reader(file)
        header = next(csvreader)

        line = 2
        failed_line = []
        for row in csvreader:
            try:
                data = {"vessel_id": row[0],
                    "received_time_utc": row[1],
                    "latitude": row[2],
                    "longitude": row[3]}

                new_vessel_position = vessel_position_creation_schema.load(data)

                if VesselPosition.query.filter_by(vessel_id=data["vessel_id"],
                                                  received_time_utc=data["received_time_utc"]) is None:
                    db.session.add(new_vessel_position)

            except:
                failed_line.append(line)

            line += 1

        db.session.commit()
        file.close()
        os.remove(os.path.join(upload_dir, secure_filename(file.filename)))

    if len(failed_line) > 0:
        message = "error format data on line: " + str(failed_line)
        return jsonify({"message": message}), 201
    else:
        return Response(status=201)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
