from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Content, AdSlot

DATABASE_URL = "postgresql://postgres:devpassword@localhost:5433/catalog"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)