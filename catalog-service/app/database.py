from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Content, AdSlot
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)