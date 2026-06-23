from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import init_db, SessionLocal, get_db
from .models import Content

app = FastAPI(title="Catalog Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    init_db()

# /content (list all) endpoint
@app.get("/content")
def list_content(db: Session = Depends(get_db)):
    return db.query(Content).all()

# /content/{id} (get 1 content) endpoint
@app.get("/content/{content_id}")
def get_content(content_id: str, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content