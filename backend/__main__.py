import csv
from backend import create_app
from flask import request, jsonify, Response
import os
from werkzeug.utils import secure_filename
from backend.models.vessel_position import VesselPosition
from backend.extensions import db
from backend.routes.vessel_positions import VesselPositionCreationSchema

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

        for row in csvreader:
            data = {"vessel_id": row[0],
                    "received_time_utc": row[1],
                    "latitude": row[2],
                    "longitude": row[3]}

            new_vessel_position = vessel_position_creation_schema.load(data)

            db.session.add(new_vessel_position)
            db.session.commit()

        file.close()
    return Response(status=204)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
