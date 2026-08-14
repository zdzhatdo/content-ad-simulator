from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from .event_publisher import publish_event
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
def watch_content(content_id: str, slot_id: str, viewer_region: str): # viewer region as query parameter only
    content_response = httpx.get(f"{CATALOG_SERVICE_URL}/content/{content_id}")
    if (content_response.status_code == 404):
        raise HTTPException(status_code=404, detail="Content not found")
    content_data = content_response.json()
    ad_slots = content_data["ad_slots"]
    valid_slot_ids = [slot["slot_id"] for slot in ad_slots]
    # validate this slot belongs to this content
    if slot_id not in valid_slot_ids:
        raise HTTPException(status_code=404, detail="Ad slot not found")
    
    # ad decision with graceful degradation since ad_decision is non-essential
    try: 
        ad_response = httpx.post(f"{AD_DECISION_SERVICE_URL}/decide", json={"content_id": content_id, "slot_id": slot_id, "viewer_region": viewer_region})
        if (ad_response.status_code == 200):
            ad_data = ad_response.json()
            if (ad_data["ad_id"] is not None):
                ad = ad_data
            else:
                ad = None
        else:
            ad = None
    except httpx.RequestError:
        ad = None

    # publish to redis for analytics
    try:
        publish_event(content_id, slot_id, ad)
    except Exception: # analytics is non-essential, log a silent failure (redis.RedisError, redis.ConnectionError, or ValueError/TypeError from json.dumps(event))
        pass

    return {"content": content_data, "ad": ad}
