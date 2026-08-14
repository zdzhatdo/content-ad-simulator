# Must load test env BEFORE importing app modules —
# redis_client.py reads REDIS_URL at import time.
# Moving this below app imports would silently connect to dev Redis instead.
from dotenv import load_dotenv
from app.subscriber import process_event

load_dotenv(".env.test")

from fastapi.testclient import TestClient
from app.main import app
from app.redis_client import r
import pytest

client = TestClient(app)

# cleanup fixture
@pytest.fixture(autouse=True)
def clean_redis():
    r.flushdb()
    yield
    r.flushdb()

# health check
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# per-content stats endpoint
def test_get_content_stats():
    # set Redis counters directly, simulating what subscriber would have written
    r.set("stats:vid_001:views", 5)
    r.set("stats:vid_001:ad_impressions", 4)
    r.set("stats:vid_001:ad_misses", 1)

    response = client.get("/stats/content/vid_001")
    assert response.status_code == 200
    assert response.json() == {
        "content_id": "vid_001",
        "views": 5,
        "ad_impressions": 4,
        "ad_misses": 1,
        "ad_miss_rate": 0.2
    }

# summary stats endpoint
def test_get_summary_stats():
    # set counters for two different content items
    r.set("stats:vid_001:views", 3)
    r.set("stats:vid_001:ad_impressions", 3)
    r.set("stats:vid_001:ad_misses", 0)
    r.set("stats:vid_002:views", 2)
    r.set("stats:vid_002:ad_impressions", 1)
    r.set("stats:vid_002:ad_misses", 1)

    response = client.get("/stats/summary")
    assert response.status_code == 200
    assert response.json() == {
        "total_views": 5,
        "total_ad_impressions": 4,
        "total_ad_misses": 1,
        "ad_miss_rate": 0.2
    }

# idempotency
def test_idempotency():
    event = {
        "event_id": "test-event-123",
        "event_type": "ad_served",
        "timestamp": "2026-07-03T18:58:16Z",
        "data": {
            "content_id": "vid_001",
            "slot_id": "slot_001",
            "ad_id": "ad_1"
        }
    }

    # process the same event twice
    process_event(event)
    process_event(event)

    # views should only be 1, not 2
    views = int(r.get("stats:vid_001:views") or 0)
    impressions = int(r.get("stats:vid_001:ad_impressions") or 0)
    assert views == 1
    assert impressions == 1