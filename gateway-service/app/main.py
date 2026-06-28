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

# /watch/{content_id}/{slot_id} called when a user is at the appropriate
# timestamp for the denoted ad slot while watching the denoted content
@app.get("/watch/{content_id}/{slot_id}")
def watch_content(content_id: str, slot_id: str):
    content_response = httpx.get(f"{CATALOG_SERVICE_URL}/content/{content_id}")
    if (content_response.status_code == 404):
        raise HTTPException(status_code=404, detail="Content not found")
    content_data = content_response.json()
    ad_slots = content_data["ad_slots"]
    valid_slot_ids = [slot["slot_id"] for slot in ad_slots]
    # validate this slot belongs to this content
    if slot_id not in valid_slot_ids:
        raise HTTPException(status_code=404, detail="Ad slot not found")
    return {"content": content_data, "slot_valid": True}
