from pydantic import BaseModel

# payload
class EventData(BaseModel):
    content_id: str
    slot_id: str
    ad_id: str | None # none for ad_missed graceful degradation case

# envelope
class AnalyticsEvent(BaseModel):
    event_id: str
    event_type: str
    timestamp: str
    data: EventData