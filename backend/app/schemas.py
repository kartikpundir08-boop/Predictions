from pydantic import BaseModel, Field
from typing import Optional, List

class CustomerPredictRequest(BaseModel):
    name: Optional[str] = Field("Guest Customer", description="Customer full name")
    frequency: float = Field(..., ge=0, description="Number of repeat purchases")
    recency: float = Field(..., ge=0, description="Days between first and last purchase")
    avg_order_value: float = Field(..., gt=0, description="Average monetary value per order (INR)")
    tenure: float = Field(..., gt=0, description="Customer age / tenure in days since first purchase")

class CustomerPredictResponse(BaseModel):
    id: Optional[int] = 1
    name: str
    frequency: float
    recency: float
    avg_order_value: float
    tenure: float
    predicted_clv: float
    segment: str
    expected_orders_next_12m: float
    expected_avg_spend: float
    recommendation: str

class CustomerRecord(BaseModel):
    id: int
    name: str
    frequency: float
    recency: float
    avg_order_value: float
    tenure: float
    predicted_clv: float
    segment: str

class ModelMetricsResponse(BaseModel):
    model_name: str
    dataset_records: int
    r2_score: float
    mae: float
    retention_cutoff_days: int
    training_status: str
