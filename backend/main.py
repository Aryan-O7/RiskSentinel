import sys
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from ml.risk_engine import assess_transaction


# --------------------------------------------------
# Create FastAPI app
# --------------------------------------------------

app = FastAPI(
    title="RiskSentinel API",
    description="AI-powered payment fraud risk detection API",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request schema
# --------------------------------------------------

class TransactionRequest(BaseModel):
    amount: float = Field(gt=0)
    account_age_days: int = Field(ge=1)
    transactions_last_24h: int = Field(ge=0)
    avg_transaction_amount: float = Field(gt=0)
    failed_attempts: int = Field(ge=0)
    device_changed: int = Field(ge=0, le=1)
    location_changed: int = Field(ge=0, le=1)
    ip_risk_score: float = Field(ge=0, le=1)
    previous_chargebacks: int = Field(ge=0)
    transaction_hour: int = Field(ge=0, le=23)
    payment_method: str


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "RiskSentinel",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Risk assessment
# --------------------------------------------------

@app.post("/api/v1/risk/assess")
def assess_risk(transaction: TransactionRequest):
    try:
        result = assess_transaction(
            transaction.model_dump()
        )

        return {
            "success": True,
            "data": result
        }

    except Exception:
        return {
            "success": False,
            "error": "Risk assessment failed"
        }
