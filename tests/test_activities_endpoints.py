"""Tests for GET /activities endpoint."""


def test_get_activities_returns_200(client):
    response = client.get("/activities")
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)


def test_get_activities_contains_seeded_activities(client):
    response = client.get("/activities")
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_each_has_required_fields(client):
    response = client.get("/activities")
    data = response.json()
    required_fields = {"description", "schedule", "max_participants", "participants"}
    for name, details in data.items():
        assert required_fields <= details.keys(), (
            f"Activity '{name}' is missing one or more required fields"
        )


def test_get_activities_participants_is_list(client):
    response = client.get("/activities")
    data = response.json()
    for name, details in data.items():
        assert isinstance(details["participants"], list), (
            f"'participants' for '{name}' should be a list"
        )


def test_get_activities_max_participants_is_int(client):
    response = client.get("/activities")
    data = response.json()
    for name, details in data.items():
        assert isinstance(details["max_participants"], int), (
            f"'max_participants' for '{name}' should be an int"
        )


def test_get_activities_seeded_participant_present(client):
    response = client.get("/activities")
    data = response.json()
    assert "existing@mergington.edu" in data["Chess Club"]["participants"]


def test_get_activities_empty_participants_list(client):
    response = client.get("/activities")
    data = response.json()
    assert data["Programming Class"]["participants"] == []
