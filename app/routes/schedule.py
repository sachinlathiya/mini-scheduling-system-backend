from flask import jsonify
from flask_cors import cross_origin

from ..services.data_service import get_data_stores
from . import api


@api.route("/schedule", methods=["GET"])
@cross_origin()
def list_schedule():
    stores = get_data_stores()
    schedule = stores["schedule"].read()
    return jsonify(schedule)


