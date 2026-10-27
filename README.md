# LifeTimeIQ: AI-Powered Customer Lifetime Value Predictor

A complete, production-grade Customer Lifetime Value (CLV) system featuring a **Python / FastAPI** probabilistic backend and a modern **HTML5 / CSS3 / Vanilla JS** responsive dashboard.

---

## Folder Structure

```
clv_project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI REST API endpoints
│   │   ├── model.py         # Probabilistic CLV engine & RFM feature transformer
│   │   ├── train.py         # Transactional dataset generation & training script
│   │   └── schemas.py       # Pydantic schema validation models
│   ├── data/                # Generated real-time RFM CSV & model artifacts
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # SPA semantic layout with authentication
│   ├── style.css            # Custom CSS properties, animations, & glassmorphism
│   └── script.js            # Frontend state, API sync, and Canvas charts
└── README.md
```

---

## Quick Setup & Execution

### 1. Start the Backend API

Open your terminal, navigate to the `backend` folder, install requirements, and run FastAPI:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will automatically initialize, generate transactional RFM data, train the baseline model, and start serving at `http://localhost:8000`. You can inspect interactive Swagger documentation at `http://localhost:8000/docs`.

### 2. Launch the Frontend

Simply open `frontend/index.html` in your web browser, or serve it using Python's built-in HTTP server:

```bash
cd frontend
python -m http.server 3000
```
Then visit `http://localhost:3000`.

---

## Default Logins

* **Admin:** `admin` / `admin123` (Full configuration access)
* **Analyst:** `analyst` / `analyst123` (Predictions, model retraining)
* **Manager:** `manager` / `manager123` (Executive reports, read-only budgeting)
