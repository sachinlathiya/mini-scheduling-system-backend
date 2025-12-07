import logging
import uuid
from typing import Dict, List, Tuple

from .data_service import get_data_stores
from ..time_utils import ranges_overlap

logger = logging.getLogger(__name__)


def validate_assignment(employee: Dict, job: Dict, schedule: List[Dict], jobs_lookup: Dict[str, Dict]) -> Tuple[bool, str]:
    if not employee.get("availability", False):
        return False, "Employee is not available right now."

    for existing in schedule:
        if existing["employeeId"] != employee["id"]:
            continue
        other_job = jobs_lookup.get(existing["jobId"])
        if not other_job:
            continue
        if ranges_overlap(job["startTime"], job["endTime"], other_job["startTime"], other_job["endTime"]):
            return False, "Employee already booked during that time slot."

    return True, ""


def create_assignment(emp_id: str, job_id: str):
    stores = get_data_stores()
    employees = stores["employees"].read()
    jobs = stores["jobs"].read()
    schedule = stores["schedule"].read()

    emp_lookup = {e["id"]: e for e in employees}
    job_lookup = {j["id"]: j for j in jobs}
    employee = emp_lookup.get(emp_id)
    job = job_lookup.get(job_id)

    if not employee or not job:
        return None, {"error": "Employee or job not found"}, 404

    ok, reason = validate_assignment(employee, job, schedule, job_lookup)
    if not ok:
        return None, {"error": reason}, 400

    assignment = {
        "id": str(uuid.uuid4()),
        "employeeId": employee["id"],
        "jobId": job["id"],
        "startTime": job["startTime"],
        "endTime": job["endTime"],
    }
    schedule.append(assignment)
    stores["schedule"].write(schedule)
    logger.info("Created assignment", extra={"assignment": assignment})
    return assignment, None, 201


def delete_assignment_by_id(assignment_id: str):
    stores = get_data_stores()
    schedule = stores["schedule"].read()
    filtered = [s for s in schedule if s["id"] != assignment_id]
    if len(filtered) == len(schedule):
        return {"error": "Assignment not found"}, 404
    stores["schedule"].write(filtered)
    logger.info("Deleted assignment", extra={"assignment_id": assignment_id})
    return None, 204



