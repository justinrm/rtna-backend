from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_feedback():
    response = client.post(
        "/feedback/add",
        json={"user_id": 1, "content_id": 101, "feedback_type": "like"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Feedback added successfully."

def test_get_feedback():
    client.post(
        "/feedback/add",
        json={"user_id": 1, "content_id": 101, "feedback_type": "like"},
    )
    response = client.get("/feedback/101")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_analyze_feedback_trends():
    client.post(
        "/feedback/add",
        json={"user_id": 1, "content_id": 101, "feedback_type": "like"},
    )
    response = client.get("/feedback/analysis")
    assert response.status_code == 200
    assert "feedback_type" in response.json()[0]

