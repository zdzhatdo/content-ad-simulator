from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Content(Base):
    __tablename__ = "content"
    id = Column(String, primary_key=True)
    title = Column(String)
    duration_seconds = Column(Integer)