# Must load test env (.env.test) BEFORE importing any app modules,
# since database.py reads DATABASE_URL from the environment at import time.
# If this load_dotenv call moves below the app imports, tests will
# silently connect to the real dev database instead of catalog_test.
from dotenv import load_dotenv
load_dotenv(".env.test")

from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import Base, engine

client = TestClient(app)

# fixture to clean between tests
@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_content():
    response = client.post("/content", json={"id": "test_vid", "title": "test_title", "duration_seconds": 1800})
    assert response.status_code == 200
    assert response.json() == {"id": "test_vid", "title": "test_title", "duration_seconds": 1800, "ad_slots": []}

def test_create_ad_slot():
    client.post("/content", json={"id": "test_vid", "title": "test_title", "duration_seconds": 1800})
    response = client.post("/content/test_vid/ad_slot", json={"slot_id": "test_ad", "offset_seconds": 0})
    assert response.status_code == 200
    assert response.json() == {"slot_id": "test_ad", "offset_seconds": 0}

# 404 get content
def test_get_content_not_found():
    response = client.get("/content/test_vid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Content not found"}

# 409 create content
def test_create_content_already_exists():
    client.post("/content", json={"id": "test_vid", "title": "test_title", "duration_seconds": 1800})
    response = client.post("/content", json={"id": "test_vid", "title": "new_title", "duration_seconds": 1200})
    assert response.status_code == 409
    assert response.json() == {"detail": "Content with this id already exists"}