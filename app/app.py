from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

Model_Path = "model.joblib"
app = FastAPI()
model = joblib.load(Model_Path)

requests_total = Counter("api_request_total", "API requests total")
prediction_latency = Histogram("api_prediction_seconds", "Prediction latency seconds")


class Tx(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V5: float; V6: float 
    V7: float; V8: float; V9: float; V10: float; V11: float; V12: float
    V13: float; V14: float; V15: float; V16: float; V17: float; V18: float
    V19: float; V20: float; V21: float; V22: float; V23: float; V24: float
    V25: float; V26: float; V27: float; V28: float; Amount: float


def features_from_tx(tx: Tx):
    vals = [getattr(tx, f) for f in sorted(tx.__fields__.keys())]
    return np.array(vals).reshape(1, -1)


@app.post("/predict")
def predict(tx: Tx):
    requests_total.inc()
    t0 = prediction_latency.time()
    X = features_from_tx(tx)
    score = model.predict_proba(X)[:,1][0]
    lbl = int(score >= 0.5)
    t0.observe_duration()
    return {"score": float(score), "label": lbl}

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}