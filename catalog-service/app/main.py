from fastapi import FastAPI
from .database import init_db

app = FastAPI(title="Catalog Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    init_db()