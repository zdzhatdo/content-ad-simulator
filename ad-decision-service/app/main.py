from fastapi import FastAPI
from .decision import decide_ad
from .schemas import DecisionRequest, DecisionResponse

app = FastAPI(title="Ad Decision Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/decide", response_model=DecisionResponse)
def make_ad_decision(decision: DecisionRequest):
    new_decision = decide_ad(decision.viewer_region)
    return new_decision