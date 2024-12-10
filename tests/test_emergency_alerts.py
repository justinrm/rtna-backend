from fastapi.testclient import TestClient
from app.main import app
from app.modules.emergency_alerts import fetch_emergency_alerts, clear_cached_alerts

client = TestClient(app)

def test_fetch_emergency_alerts(mocker):
    mocker.patch("app.modules.emergency_alerts.fetch_emergency_alerts", return_value=[{"alert": "Test Alert"}])
    response = client.get("/alerts/Lewiston")
    assert response.status_code == 200
    assert response.json()["alerts"] == [{"alert": "Test Alert"}]

def test_clear_cached_alerts(mocker):
    mocker.patch("app.modules.emergency_alerts.clear_cached_alerts", return_value={"message": "Cache cleared."})
    response = client.delete("/alerts/Lewiston/cache")
    assert response.status_code == 200
    assert response.json()["message"] == "Cache cleared."

