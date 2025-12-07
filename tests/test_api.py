import json
import os
from pathlib import Path

import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "employees.json").write_text(
        json.dumps(
            [
                {"id": "e1", "name": "Sam", "role": "TCP", "availability": True},
                {"id": "e2", "name": "Rita", "role": "LCT", "availability": False},
            ]
        )
    )
    (data_dir / "jobs.json").write_text(
        json.dumps(
            [
                {"id": "j1", "name": "Job 1", "startTime": "08:00", "endTime": "10:00"},
                {"id": "j2", "name": "Job 2", "startTime": "09:00", "endTime": "11:00"},
            ]
        )
    )
    (data_dir / "schedule.json").write_text(json.dumps([]))
    monkeypatch.setenv("DATA_DIR", str(data_dir))
    app = create_app()
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_assign_happy_path(client):
    resp = client.post("/assign", json={"employeeId": "e1", "jobId": "j1"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["employeeId"] == "e1"
    assert body["jobId"] == "j1"


def test_assign_reject_unavailable(client):
    resp = client.post("/assign", json={"employeeId": "e2", "jobId": "j1"})
    assert resp.status_code == 400
    assert "available" in resp.get_json()["error"]


def test_assign_overlapping_blocked(client):
    first = client.post("/assign", json={"employeeId": "e1", "jobId": "j1"})
    assert first.status_code == 201
    resp = client.post("/assign", json={"employeeId": "e1", "jobId": "j2"})
    assert resp.status_code == 400
    assert "booked" in resp.get_json()["error"]


