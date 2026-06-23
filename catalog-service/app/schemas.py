from pydantic import BaseModel

class ContentCreate(BaseModel):
    id: str
    title: str
    duration_seconds: int

class AdSlotResponse(BaseModel):
    slot_id: str
    offset_seconds: int

    class Config:
        from_attributes = True

class ContentResponse(BaseModel):
    id: str
    title: str
    duration_seconds: int
    ad_slots: list[AdSlotResponse]
    class Config:
        from_attributes = True