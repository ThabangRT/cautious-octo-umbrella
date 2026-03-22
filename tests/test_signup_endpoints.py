"""Tests for POST /activities/{activity_name}/signup
and DELETE /activities/{activity_name}/signup endpoints."""

import pytest

# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )
    assert response.status_code == 200
    assert "newstudent@mergington.edu" in response.json()["message"]


def test_signup_participant_appears_in_activities(client):
    client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_activity_not_found_returns_404(client):
    response = client.post(
        "/activities/Nonexistent%20Club/signup",
        params={"email": "student@mergington.edu"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "existing@mergington.edu"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_into_empty_activity(client):
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": "first@mergington.edu"},
    )
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert "first@mergington.edu" in activities["Programming Class"]["participants"]


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_unregister_success(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "existing@mergington.edu"},
    )
    assert response.status_code == 200
    assert "existing@mergington.edu" in response.json()["message"]


def test_unregister_participant_removed_from_activities(client):
    client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "existing@mergington.edu"},
    )
    activities = client.get("/activities").json()
    assert "existing@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_activity_not_found_returns_404(client):
    response = client.delete(
        "/activities/Nonexistent%20Club/signup",
        params={"email": "existing@mergington.edu"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_enrolled_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "notenrolled@mergington.edu"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_signup_then_unregister_roundtrip(client):
    """Sign up a student then immediately unregister — list should be back to original."""
    email = "roundtrip@mergington.edu"
    client.post("/activities/Programming%20Class/signup", params={"email": email})
    client.delete("/activities/Programming%20Class/signup", params={"email": email})
    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]


def test_unregister_does_not_affect_other_activities(client):
    """Removing a participant from one activity must not touch other activities."""
    client.delete(
        "/activities/Chess%20Club/signup",
        params={"email": "existing@mergington.edu"},
    )
    activities = client.get("/activities").json()
    # Programming Class should be unchanged
    assert activities["Programming Class"]["participants"] == []
