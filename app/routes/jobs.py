from flask import jsonify
from flask_cors import cross_origin

from ..services.data_service import get_data_stores
from . import api


@api.route("/jobs", methods=["GET"])
@cross_origin()
def list_jobs():
    stores = get_data_stores()
    jobs = stores["jobs"].read()
    return jsonify(jobs)


