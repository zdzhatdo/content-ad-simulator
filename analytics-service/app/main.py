from fastapi import FastAPI
from .redis_client import r
import threading
from .subscriber import start_subscriber

app = FastAPI(title="Analytics Service")

@app.on_event("startup")
def on_startup():
    r.ping()
    thread = threading.Thread(target=start_subscriber, daemon=True)
    thread.start()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/stats/content/{content_id}")
def get_content_stats(content_id: str):
    views = int(r.get(f"stats:{content_id}:views") or 0)
    impressions = int(r.get(f"stats:{content_id}:ad_impressions") or 0)
    misses = int(r.get(f"stats:{content_id}:ad_misses") or 0)
    ad_miss_rate = misses / views if views > 0 else 0.0

    return {
        "content_id": content_id,
        "views": views,
        "ad_impressions": impressions,
        "ad_misses": misses,
        "ad_miss_rate": ad_miss_rate
    }

@app.get("/stats/summary")
def get_summary_stats():
    keys = r.keys("stats:*:views")
    
    total_views = 0
    total_impressions = 0
    total_misses = 0

    for key in keys:
        content_id = key.decode().split(":")[1]
        total_views += int(r.get(f"stats:{content_id}:views") or 0)
        total_impressions += int(r.get(f"stats:{content_id}:ad_impressions") or 0)
        total_misses += int(r.get(f"stats:{content_id}:ad_misses") or 0)

    ad_miss_rate = total_misses / total_views if total_views > 0 else 0.0

    return {
        "total_views": total_views,
        "total_ad_impressions": total_impressions,
        "total_ad_misses": total_misses,
        "ad_miss_rate": ad_miss_rate
    }