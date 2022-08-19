import pytest
from sqlalchemy import delete

from backend import create_app, db
from backend.models.vessel_position import VesselPosition


@pytest.fixture(scope="session")
def flask_app():
    app = create_app()

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture
def app_with_data(app_with_db):
    vessel_position = VesselPosition(vessel_id=11111,
                                     received_time_utc="2006-12-21 12:09:04.000000",
                                     latitude=56.1234,
                                     longitude=-67.3456
                                     )
    db.session.add(vessel_position)

    db.session.commit()

    yield app_with_db

    db.session.delete(vessel_position)
    db.session.commit()
