import logging
from logging.config import dictConfig
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
from shutil import copy2

from .config import load_config
from .routes import api


def configure_logging(level: str):
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {"level": level, "handlers": ["console"]},
        }
    )


def seed_data_dir(app):
    data_dir = app.config["DATA_DIR"]
    src_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    for name in ["employees.json", "jobs.json", "schedule.json"]:
        dst = data_dir / name
        if not dst.exists():
            copy2(src_dir / name, dst)


def create_app():
    load_dotenv()
    config = load_config()
    configure_logging(config.LOG_LEVEL)
    app = Flask(__name__)
    app.config.from_object(config)
    seed_data_dir(app)

    CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})
    app.register_blueprint(api)
    return app


