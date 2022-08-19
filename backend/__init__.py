from flask import Flask
from backend.routes.vessel_positions import vp_bp
from backend.routes.error import error_bp
from backend.extensions import db


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "postgresql://user:password@localhost:5432/backenddb"

    # enable debugging mode
    app.config["DEBUG"] = True

    db.app = app
    db.init_app(app)
    db.create_all()

    app.register_blueprint(vp_bp)
    app.register_blueprint(error_bp)

    return app
