from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "Test123!@"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully."

def test_login_user():
    client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "Test123!@"},
    )
    response = client.post(
        "/users/token",
        data={"username": "test@example.com", "password": "Test123!@"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

