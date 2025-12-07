from flask import Blueprint

api = Blueprint("api", __name__)

# Import route modules to attach handlers to the shared blueprint
from . import employees, jobs, schedule, assignments  # noqa: E402,F401


