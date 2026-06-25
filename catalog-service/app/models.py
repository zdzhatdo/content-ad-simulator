from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Content(Base):
    __tablename__ = "content"
    id = Column(String, primary_key=True)
    title = Column(String)
    duration_seconds = Column(Integer)
    ad_slots = relationship("AdSlot")

class AdSlot(Base):
    __tablename__ = "adslot"
    slot_id = Column(String, primary_key=True)
    offset_seconds = Column(Integer)
    content_id = Column(String, ForeignKey("content.id"))