from fastapi.testclient import TestClient
from app.main import app
import httpx

client = TestClient(app)

# fake responses for monkeypatching
class FakeResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data

    def json(self):
        return self._json_data

# complete success, content and ad delivered successfully
def test_watch_content_success(monkeypatch):
    def fake_get(url, **kwargs):
        return FakeResponse(200, {"id": "vid_001", "title": "Test", "duration_seconds": 100, "ad_slots": [{"slot_id": "slot_1", "offset_seconds": 0}]})

    def fake_post(url, **kwargs):
        return FakeResponse(200, {"ad_id": "ad_1", "ad_duration_seconds": 15, "decision_reason": "Region match"})

    monkeypatch.setattr("app.main.httpx.get", fake_get)
    monkeypatch.setattr("app.main.httpx.post", fake_post)

    response = client.get("/watch/vid_001/slot_1?viewer_region=NJ")
    assert response.status_code == 200

# 404: content not found
def test_watch_content_not_found(monkeypatch):
    def fake_get(url, **kwargs):
        return FakeResponse(404, {})
    monkeypatch.setattr("app.main.httpx.get", fake_get)
    response = client.get("/watch/non_vid/slot_1?viewer_region=NJ")
    assert response.status_code == 404

# 404: content found, but slot not found
def test_watch_slot_not_found(monkeypatch):
    def fake_get(url, **kwargs):
        return FakeResponse(200, {"id": "vid_001", "title": "Test", "duration_seconds": 100, "ad_slots": []})
    
    monkeypatch.setattr("app.main.httpx.get", fake_get)
    response = client.get("/watch/vid_001/slot_1?viewer_region=NJ")
    assert response.status_code == 404

# 200, no ad available
def test_watch_no_ad_available(monkeypatch):
    def fake_get(url, **kwargs):
        return FakeResponse(200, {"id": "vid_001", "title": "Test", "duration_seconds": 100, "ad_slots": [{"slot_id": "slot_1", "offset_seconds": 0}]})

    def fake_post(url, **kwargs):
        return FakeResponse(200, {"ad_id": None, "ad_duration_seconds": None, "decision_reason": "No ad available"})

    monkeypatch.setattr("app.main.httpx.get", fake_get)
    monkeypatch.setattr("app.main.httpx.post", fake_post)

    response = client.get("/watch/vid_001/slot_1?viewer_region=ZZ")
    assert response.status_code == 200
    assert response.json()["ad"] == None

# 200 ad service down (failure)
def test_watch_ad_down(monkeypatch):
    def fake_get(url, **kwargs):
        return FakeResponse(200, {"id": "vid_001", "title": "Test", "duration_seconds": 100, "ad_slots": [{"slot_id": "slot_1", "offset_seconds": 0}]})
    
    def fake_post(url, **kwargs):
        raise httpx.RequestError("Connection failed")
    
    monkeypatch.setattr("app.main.httpx.get", fake_get)
    monkeypatch.setattr("app.main.httpx.post", fake_post)

    response = client.get("/watch/vid_001/slot_1?viewer_region=NJ")
    assert response.status_code == 200
    assert response.json()["ad"] == None