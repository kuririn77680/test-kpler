from flask import jsonify, Blueprint
from werkzeug.exceptions import NotFound

error_bp = Blueprint("errors", __name__)


@error_bp.app_errorhandler(NotFound)
def handle_not_found(err):
    return jsonify({"message": "Ressource not founded"}), 404


@error_bp.app_errorhandler(Exception)
def handle_generic_exception(err):
    return jsonify({"message": "Unknown error"}), 500
