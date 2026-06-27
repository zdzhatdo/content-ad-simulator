from pydantic import BaseModel

class DecisionRequest(BaseModel):
    content_id: str
    slot_id: str
    viewer_region: str
    
class DecisionResponse(BaseModel):
    ad_id: str | None
    ad_duration_seconds: int | None
    decision_reason: str