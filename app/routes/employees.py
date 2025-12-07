from flask import jsonify
from flask_cors import cross_origin

from ..services.data_service import get_data_stores
from . import api


@api.route("/employees", methods=["GET"])
@cross_origin()
def list_employees():
    stores = get_data_stores()
    employees = stores["employees"].read()
    return jsonify(employees)


