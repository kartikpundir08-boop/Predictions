import os
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from backend.app.schemas import (
    CustomerPredictRequest, CustomerPredictResponse,
    CustomerRecord, ModelMetricsResponse
)
from backend.app.model import CLVEngine
from backend.app.train import DATA_PATH, generate_and_train

app = FastAPI(title="LifeTimeIQ CLV Engine", version="2.0.0")

# Enable Cross-Origin Resource Sharing for seamless frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = CLVEngine()

@app.on_event("startup")
def startup_event():
    if not os.path.exists(DATA_PATH):
        generate_and_train()
    engine.load()

SEGMENT_RECOMMENDATIONS = {
    "Platinum": "Protect & Reward: Assign VIP concierge, offer early-access product launches, bespoke loyalty rewards.",
    "Gold": "Grow & Nurture: Offer cross-sell bundles, tier upgrade incentives, and proactive customer satisfaction check-ins.",
    "Silver": "Re-engage & Activate: Send targeted reactivation discounts, win-back sequence via email/SMS.",
    "Bronze": "Automate Efficiently: Maintain automated email newsletters; minimize paid retention spend."
}

@app.get("/")
def health_check():
    return {"status": "online", "model": "LifeTimeIQ Production CLV Engine"}

@app.post("/api/predict", response_model=CustomerPredictResponse)
def predict_clv(req: CustomerPredictRequest):
    if req.recency > req.tenure:
        raise HTTPException(status_code=400, detail="Recency cannot be greater than total customer tenure.")

    predicted_clv, segment, exp_orders, exp_aov = engine.predict(
        frequency=req.frequency,
        recency=req.recency,
        avg_order_value=req.avg_order_value,
        tenure=req.tenure
    )

    return CustomerPredictResponse(
        id=1,
        name=req.name,
        frequency=req.frequency,
        recency=req.recency,
        avg_order_value=req.avg_order_value,
        tenure=req.tenure,
        predicted_clv=predicted_clv,
        segment=segment,
        expected_orders_next_12m=exp_orders,
        expected_avg_spend=exp_aov,
        recommendation=SEGMENT_RECOMMENDATIONS.get(segment, "")
    )

@app.get("/api/customers", response_model=List[CustomerRecord])
def get_customers(limit: int = 250):
    if not os.path.exists(DATA_PATH):
        generate_and_train()
        engine.load()
    
    df = pd.read_csv(DATA_PATH).head(limit)
    records = []
    for _, row in df.iterrows():
        clv, seg, _, _ = engine.predict(
            row["frequency"], row["recency"], row["avg_order_value"], row["tenure"]
        )
        records.append(CustomerRecord(
            id=int(row["id"]),
            name=str(row["name"]),
            frequency=float(row["frequency"]),
            recency=float(row["recency"]),
            avg_order_value=float(row["avg_order_value"]),
            tenure=float(row["tenure"]),
            predicted_clv=clv,
            segment=seg
        ))
    return records

@app.get("/api/metrics", response_model=ModelMetricsResponse)
def get_metrics():
    df_count = len(pd.read_csv(DATA_PATH)) if os.path.exists(DATA_PATH) else 1500
    return ModelMetricsResponse(
        model_name="Ridge-Regularized Probabilistic RFM Regressor",
        dataset_records=df_count,
        r2_score=engine.r2,
        mae=engine.mae,
        retention_cutoff_days=180,
        training_status="Active & Serving"
    )

@app.post("/api/retrain")
def retrain_model():
    generate_and_train()
    engine.load()
    return {"message": "Model retrained and loaded successfully", "r2": engine.r2, "mae": engine.mae}
