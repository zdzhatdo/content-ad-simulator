from fastapi import FastAPI
from .redis_client import r

app = FastAPI(title="Analytics Service")

@app.on_event("startup")
def on_startup():
    r.ping()

@app.get("/health")
def health_check():
    return {"status": "ok"}