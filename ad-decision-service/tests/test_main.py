from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# match for exact user region
def test_decide_region_match():
    response = client.post("/decide", json={"content_id": "test_vid", "slot_id": "slot_1", "viewer_region": "NJ"})
    assert response.status_code == 200
    assert response.json() == {"ad_id": "ad_1", "ad_duration_seconds": 15, "decision_reason": "Region match"}

# fallback (ad with no region)
def test_decide_fallback():
    response = client.post("/decide", json={"content_id": "test_vid", "slot_id": "slot_1", "viewer_region": "other-region"})
    assert response.status_code == 200
    assert response.json() == {"ad_id": "ad_3", "ad_duration_seconds": 30, "decision_reason": "Fallback"}

# no ad found (no region match and no alternatives)
def test_decide_no_ad_available(monkeypatch):
    monkeypatch.setattr("app.decision.get_ad_inventory", lambda: [])
    response = client.post("/decide", json={"content_id": "test_vid", "slot_id": "slot_1", "viewer_region": "ZZ"})
    assert response.status_code == 200
    assert response.json() == {"ad_id": None, "ad_duration_seconds": None, "decision_reason": "No ad available"}
