import io
from datetime import datetime

from flask import url_for
from backend.models.vessel_position import VesselPosition


def test_get_all_vessel_position(app_with_data):
    response = app_with_data.get(url_for("vessel_positions.get_all_vessel_position"))

    assert response.status_code == 200
    vessel_positions = VesselPosition.query.all()
    count = len(vessel_positions)

    assert count == 1

    for vessel_position in vessel_positions:
        assert vessel_position.vessel_id == 11111
        assert vessel_position.received_time_utc == datetime(2006, 12, 21, 12, 9, 4)
        assert vessel_position.latitude == 56.1234
        assert vessel_position.longitude == -67.3456


def test_get_vessel_position(app_with_data):
    response = app_with_data.get(url_for("vessel_positions.get_vessel_position", vessel_id=11111))

    assert response.status_code == 200
    vessel_positions = VesselPosition.query.all()
    count = len(vessel_positions)
    assert count == 1

    for vessel_position in vessel_positions:
        assert vessel_position.vessel_id == 11111
        assert vessel_position.received_time_utc == datetime(2006, 12, 21, 12, 9, 4)
        assert vessel_position.latitude == 56.1234
        assert vessel_position.longitude == -67.3456


def test_add_vessel_position(app_with_db):
    response = app_with_db.post(url_for("vessel_positions.add_vessel_position"),
                                json={
                                    "vessel_id": 12345,
                                    "received_time_utc": "2016-12-21 12:09:04.000000",
                                    "latitude": 70.8765,
                                    "longitude": 12.09894
                                })

    assert response.status_code == 201
    vessel_positions = VesselPosition.query.filter_by(vessel_id=12345).all()
    count = len(vessel_positions)
    assert count == 1

    for vessel_position in vessel_positions:
        assert vessel_position.vessel_id == 12345
        assert vessel_position.received_time_utc == datetime(2016, 12, 21, 12, 9, 4)
        assert vessel_position.latitude == 70.8765
        assert vessel_position.longitude == 12.09894
