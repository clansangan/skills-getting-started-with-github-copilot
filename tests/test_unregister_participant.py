from fastapi.testclient import TestClient

from src.app import app, activities


def setup_function():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_unregister_participant_removes_email_from_activity():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "daniel@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered daniel@mergington.edu from Chess Club"
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_errors_when_not_found():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "alex@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
