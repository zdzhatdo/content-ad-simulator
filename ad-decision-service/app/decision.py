from .ad_inventory import get_ad_inventory

# Function to generate ad decision given user region
def decide_ad(viewer_region: str):
    ads = get_ad_inventory()
    decision = None
    decision_reason = None
    for ad in ads:
        if (ad["region"] == viewer_region):
            decision = ad
            decision_reason = "Region match"
            break
    if (decision == None):
        for ad in ads:
            if (ad["region"] == None):
                decision = ad
                decision_reason = "Fallback"
                break
    if (decision == None):
        return {"ad_id": None, "ad_duration_seconds": None, "decision_reason": "No ad available"}
    return {"ad_id": decision["ad_id"], "ad_duration_seconds": decision["ad_duration_seconds"], "decision_reason": decision_reason}