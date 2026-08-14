import os
import json
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]
r = redis.from_url(REDIS_URL)

EVENTS_CHANNEL = "events"

def publish_event(content_id: str, slot_id: str, ad: dict | None):
    event_type = "ad_served" if ad is not None else "ad_missed"
    
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "content_id": content_id,
            "slot_id": slot_id,
            "ad_id": ad["ad_id"] if ad is not None else None
        }
    }
    
    r.publish(EVENTS_CHANNEL, json.dumps(event))