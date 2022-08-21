from datetime import datetime

import pytest
from backend.dto.vessel_position import VesselPositionCreationSchema
from marshmallow import ValidationError


@pytest.mark.parametrize(
    "latitude,valid",
    [
        (-29.520007, True),
        (-30, True),
        (52.520007, False),
        (52, False),
        (-93, False),
        (93.234, False),
        (93, False),
        (-93.234, False),
        ("test", False),
    ]
)
def test_validate_latitude(latitude, valid):
    schema = VesselPositionCreationSchema()
    data = {"vessel_id": 2222222,
            "received_time_utc": "2022-08-21 12:09:04.000000",
            "latitude": latitude,
            "longitude": 34.404954
            }

    try:
        vessel_position = schema.load(data)
        assert valid

        assert vessel_position is not None
        assert vessel_position.vessel_id == data["vessel_id"]
        assert vessel_position.received_time_utc == datetime(2022, 8, 21, 12, 9, 4)
        assert vessel_position.latitude == latitude
        assert vessel_position.longitude == data["longitude"]

    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "longitude,valid",
    [
        (25.89009345670, False),
        (25, False),
        (-29.520007, True),
        (-30, True),
        (217.7867, False),
        (217, False),
        (-217.7867, False),
        (-217, False),
        ("test", False),
    ]
)
def test_validate_longitude(longitude, valid):
    schema = VesselPositionCreationSchema()
    data = {"vessel_id": 2222222,
            "received_time_utc": "2022-08-21 12:09:04.000000",
            "latitude": -29.520007,
            "longitude": longitude
            }

    try:
        vessel_position = schema.load(data)
        assert valid

        assert vessel_position is not None
        assert vessel_position.vessel_id == data["vessel_id"]
        assert vessel_position.received_time_utc == datetime(2022, 8, 21, 12, 9, 4)
        assert vessel_position.latitude == data["latitude"]
        assert vessel_position.longitude == longitude

    except ValidationError:
        assert not valid


@pytest.mark.parametrize(
    "latitude,longitude,valid",
    [
        (-29.520007, 34.404954, True),
        (52.520007, 34.404954, False)
    ]
)
def test_validate_vessel_position(latitude, longitude, valid):
    schema = VesselPositionCreationSchema()
    data = {"vessel_id": 2222222,
            "received_time_utc": "2022-08-21 12:09:04.000000",
            "latitude": latitude,
            "longitude": longitude
            }

    try:
        vessel_position = schema.load(data)
        assert valid

        assert vessel_position is not None
        assert vessel_position.vessel_id == data["vessel_id"]
        assert vessel_position.received_time_utc == datetime(2022, 8, 21, 12, 9, 4)
        assert vessel_position.latitude == latitude
        assert vessel_position.longitude == longitude

    except ValidationError:
        assert not valid


def test_missing_fields():
    schema = VesselPositionCreationSchema()
    data = {"vessel_id": 2222222,
            "latitude": 86.52161,
            "longitude": -56.23456
            }

    with pytest.raises(ValidationError):
        schema.load(data)
