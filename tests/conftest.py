import copy
import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

# Compact canonical test dataset — deterministic, minimal, covers all cases
TEST_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["existing@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": [],
    },
}


@pytest.fixture
def client(monkeypatch):
    """Return a TestClient with a fresh copy of TEST_ACTIVITIES for every test."""
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(TEST_ACTIVITIES))
    return TestClient(app)
