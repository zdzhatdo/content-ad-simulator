from fastapi import FastAPI
from .redis_client import r
import threading
from .subscriber import start_subscriber

app = FastAPI(title="Analytics Service")

@app.on_event("startup")
def on_startup():
    r.ping()
    thread = threading.Thread(target=start_subscriber, daemon=True)
    thread.start()

@app.get("/health")
def health_check():
    return {"status": "ok"}