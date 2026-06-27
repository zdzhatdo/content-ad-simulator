from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

CATALOG_SERVICE_URL = os.environ["CATALOG_SERVICE_URL"]
AD_DECISION_SERVICE_URL = os.environ["AD_DECISION_SERVICE_URL"]

app = FastAPI(title="Gateway Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}

# /watch/{content_id}
@app.get("/watch/{content_id}")
def watch_content(content_id: str):
    response = httpx.get(f"{CATALOG_SERVICE_URL}/content/{content_id}")
    if (response.status_code == 404):
        raise HTTPException(status_code=404, detail="Content not found")
    data = response.json()
    return data
