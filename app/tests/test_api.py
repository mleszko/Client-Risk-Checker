from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_check_risk():
    response = client.post("/check_risk", json={
        "name": "Acme Corp",
        "industry": "crypto",
        "description": "A startup under investigation for money laundering."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] == "high"
