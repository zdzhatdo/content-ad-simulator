from dotenv import load_dotenv
load_dotenv(".env.test")

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)