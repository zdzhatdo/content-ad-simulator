import json
import redis
from .redis_client import r, REDIS_URL

def process_event(event_data: dict):
    """Process a single event and update Redis counters."""
    data = event_data.get("data", {})
    content_id = data.get("content_id")
    event_type = event_data.get("event_type")
    
    if not content_id or not event_type:
        return
    
    # increment view count for this content
    r.incr(f"stats:{content_id}:views")
    
    # increment ad impression or miss count
    if event_type == "ad_served":
        r.incr(f"stats:{content_id}:ad_impressions")
    elif event_type == "ad_missed":
        r.incr(f"stats:{content_id}:ad_misses")

def start_subscriber():
    pubsub = r.pubsub()
    pubsub.subscribe("events")
    for message in pubsub.listen():
        if (message["type"] == "message"):
            event_data = json.loads(message["data"])
            process_event(event_data)