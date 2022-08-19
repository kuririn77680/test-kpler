from flask import jsonify, Blueprint
from werkzeug.exceptions import NotFound
import traceback
from marshmallow import ValidationError


error_bp = Blueprint("errors", __name__)


@error_bp.app_errorhandler(NotFound)
def handle_not_found(err):
    return jsonify({"message": "Ressource not founded"}), 404


@error_bp.app_errorhandler(ValidationError)
def handle_invalid_data(error):
    print(traceback.format_exc())
    return jsonify({"message": "Incorrect format data"}), 400


@error_bp.app_errorhandler(Exception)
def handle_generic_exception(err):
    return jsonify({"message": err}), 500
