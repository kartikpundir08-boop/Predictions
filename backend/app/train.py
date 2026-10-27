import os
import numpy as np
import pandas as pd
from backend.app.model import CLVEngine

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "customers_rfm.csv")

def generate_and_train():
    """
    Simulates real-world retail transactional data derived from UCI Online Retail distribution
    and trains the CLVEngine.
    """
    np.random.seed(42)
    n_samples = 1500

    tenure = np.random.uniform(30, 730, n_samples) # customer age between 1 month and 2 years
    # Repeat purchase counts follow Poisson / negative binomial behavior
    frequency = np.random.negative_binomial(n=2, p=0.25, size=n_samples)
    recency = np.array([np.random.uniform(0, t) for t in tenure])
    # Monetary values follow log-normal distribution
    avg_order_value = np.round(np.random.lognormal(mean=4.2, sigma=0.75, size=n_samples), 2)

    # Actual 12m forward spend generated with stochastic noise & realistic churn dynamics
    annual_rate = (frequency / tenure) * 365.0
    churn_prob = 1.0 / (1.0 + np.exp(-(recency - 160) / 45.0)) # logistic churn curve
    active_factor = 1.0 - churn_prob
    future_orders = np.maximum(0, annual_rate * active_factor * np.random.uniform(0.85, 1.15, n_samples))
    actual_future_spend = np.round(future_orders * avg_order_value, 2)

    df = pd.DataFrame({
        "id": np.arange(1001, 1001 + n_samples),
        "name": [f"Customer_{i}" for i in range(1, n_samples + 1)],
        "frequency": frequency,
        "recency": np.round(recency, 1),
        "avg_order_value": avg_order_value,
        "tenure": np.round(tenure, 1),
        "actual_future_spend": actual_future_spend
    })

    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Dataset generated at {DATA_PATH} with {n_samples} records.")

    engine = CLVEngine()
    engine.train_from_rfm(df)
    print(f"Model successfully trained! R2: {engine.r2}, MAE: INR {engine.mae}")

if __name__ == "__main__":
    generate_and_train()
