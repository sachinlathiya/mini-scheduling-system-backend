from flask import current_app

from ..storage import JsonStorage


def get_data_stores():
    base_dir = current_app.config["DATA_DIR"]
    return {
        "employees": JsonStorage(base_dir / "employees.json"),
        "jobs": JsonStorage(base_dir / "jobs.json"),
        "schedule": JsonStorage(base_dir / "schedule.json"),
    }



