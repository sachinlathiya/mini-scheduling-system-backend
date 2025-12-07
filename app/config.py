import os
from pathlib import Path


class Config:
    DATA_DIR = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parent.parent / "data"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    SECRET_KEY = os.getenv("SECRET_KEY", "changeme-in-prod")


def load_config():
    return Config()


