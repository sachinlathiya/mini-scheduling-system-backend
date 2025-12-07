from flask import jsonify, request
from flask_cors import cross_origin

from ..services.assignment_service import create_assignment, delete_assignment_by_id
from . import api


@api.route("/assign", methods=["POST"])
@cross_origin()
def assign_employee():
    payload = request.get_json(force=True, silent=True) or {}
    emp_id = payload.get("employeeId")
    job_id = payload.get("jobId")
    if not emp_id or not job_id:
        return jsonify({"error": "employeeId and jobId are required"}), 400

    assignment, error, status = create_assignment(emp_id, job_id)
    if error:
        return jsonify(error), status
    return jsonify(assignment), status


@api.route("/assign/<assignment_id>", methods=["DELETE"])
@cross_origin()
def delete_assignment(assignment_id):
    error, status = delete_assignment_by_id(assignment_id)
    if error:
        return jsonify(error), status
    return "", status


