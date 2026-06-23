from fastapi import FastAPI

app = FastAPI(title="Catalog Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}