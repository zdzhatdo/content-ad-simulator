from pydantic import BaseModel

class ContentCreate(BaseModel):
    id: str
    title: str
    duration_seconds: int