from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_risk_high():
    payload = {
        "customer_id": "API_TEST_001",
        "contract_type": "Month-to-Month",
        "monthly_charge": 75.0,
        "tickets": [
            {"ticket_id": f"T{i}", "days_ago": 5, "category": "technical"}
            for i in range(6)
        ]
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_level"] == "HIGH"

def test_predict_risk_low():
    payload = {
        "customer_id": "API_TEST_002",
        "contract_type": "Two Year",
        "monthly_charge": 90.0,
        "tickets": []
    }
    response = client.post("/predict-risk", json=payload)
    assert response.status_code == 200
    assert response.json()["risk_level"] == "LOW"

def test_missing_field_returns_error():
    response = client.post("/predict-risk", json={"customer_id": "X"})
    assert response.status_code == 422