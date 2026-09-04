import sys
import os
import logging
from pathlib import Path

# Fix import path
BACKEND_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BACKEND_DIR))

from typing import Optional
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import Base, engine, get_db
from models import Transaction, Customer
from schemas import (
    TransactionRequest,
    NewTransactionRequest,
    CustomerRequest
)
from services.risk_service import assess_risk
from services.ai_investigator import investigate_transaction
from services.report_service import get_model_metrics
from services.customer_history import get_customer_history


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("risksentinel")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RiskSentinel API",
    description="API for the RiskSentinel fraud detection system.",
    version="1.0.0"
)

# CORS
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.get("/")
def root():
    return {
        "service": "RiskSentinel",
        "status": "running"
    }

@app.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "unavailable"
            }
        )

@app.post("/api/v1/risk/assess")
def assess_transaction(
    transaction: TransactionRequest,
    db: Session = Depends(get_db)
):
    try:
        transaction_data = transaction.model_dump()
        result = assess_risk(transaction_data)

        db_transaction = Transaction(
            amount=transaction.amount,
            account_age_days=transaction.account_age_days,
            transactions_last_24h=transaction.transactions_last_24h,
            avg_transaction_amount=transaction.avg_transaction_amount,
            failed_attempts=transaction.failed_attempts,
            device_changed=transaction.device_changed,
            location_changed=transaction.location_changed,
            ip_risk_score=transaction.ip_risk_score,
            previous_chargebacks=transaction.previous_chargebacks,
            transaction_hour=transaction.transaction_hour,
            payment_method=transaction.payment_method,

            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            recommended_action=result["recommended_action"],

            risk_reasons="||".join(
                result["reasons"]
            )
        )

        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        logger.info(
            "Risk assessment created: transaction_id=%s",
            db_transaction.id
        )

        return {
            "success": True,
            "transaction_id": db_transaction.id,
            "data": result
        }

    except Exception:
        db.rollback()
        logger.exception("Risk assessment failed")
        raise HTTPException(
            status_code=500,
            detail="Risk assessment failed"
        )


# --------------------------------------------------
# Get transaction history
# --------------------------------------------------
@app.get("/api/v1/transactions")
def get_transactions(
    limit: int = 50,
    risk_level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if risk_level:
        query = query.filter(
            Transaction.risk_level == risk_level.upper()
        )

    transactions = (
        query
        .order_by(Transaction.created_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "success": True,
        "count": len(transactions),
        "data": [
            {
                "id": t.id,
                "amount": t.amount,
                "payment_method": t.payment_method,
                "risk_score": t.risk_score,
                "risk_level": t.risk_level,
                "recommended_action": t.recommended_action,
                "risk_reasons": (
                    t.risk_reasons.split("||")
                    if t.risk_reasons
                    else []
                ),
                "review_decision": t.review_decision,
                "reviewed_at": t.reviewed_at,
                "created_at": t.created_at
            }
            for t in transactions
        ]
    }

# --------------------------------------------------
# Get a single transaction
# --------------------------------------------------
@app.get("/api/v1/transactions/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "success": True,
        "data": {
            "id": transaction.id,
            "amount": transaction.amount,
            "account_age_days": transaction.account_age_days,
            "transactions_last_24h": transaction.transactions_last_24h,
            "avg_transaction_amount": transaction.avg_transaction_amount,
            "failed_attempts": transaction.failed_attempts,
            "device_changed": transaction.device_changed,
            "location_changed": transaction.location_changed,
            "ip_risk_score": transaction.ip_risk_score,
            "previous_chargebacks": transaction.previous_chargebacks,
            "transaction_hour": transaction.transaction_hour,
            "payment_method": transaction.payment_method,
            "risk_score": transaction.risk_score,
            "risk_level": transaction.risk_level,
            "recommended_action": transaction.recommended_action,
            "risk_reasons": (
                transaction.risk_reasons.split("||")
                if transaction.risk_reasons
                else []
            ),
            "review_decision": transaction.review_decision,
            "reviewed_at": transaction.reviewed_at,
            "created_at": transaction.created_at
        }
    }


# --------------------------------------------------
# Submit human review decision
# --------------------------------------------------
@app.post("/api/v1/transactions/{transaction_id}/review")
def review_transaction(
    transaction_id: int,
    decision: str,
    db: Session = Depends(get_db)
):
    allowed_decisions = {"ALLOW", "REVIEW", "BLOCK"}
    decision = decision.upper()

    if decision not in allowed_decisions:
        raise HTTPException(
            status_code=400,
            detail="Decision must be ALLOW, REVIEW, or BLOCK"
        )

    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.review_decision = decision
    transaction.reviewed_at = datetime.utcnow()

    db.commit()
    db.refresh(transaction)

    return {
        "success": True,
        "message": "Review decision saved",
        "data": {
            "transaction_id": transaction.id,
            "review_decision": transaction.review_decision,
            "reviewed_at": transaction.reviewed_at
        }
    }


@app.post("/api/v1/transactions/{transaction_id}/investigate")
def investigate_saved_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    reasons = (
        transaction.risk_reasons.split("||")
        if transaction.risk_reasons
        else []
    )

    transaction_data = {
        "amount": transaction.amount,
        "account_age_days": transaction.account_age_days,
        "transactions_last_24h": transaction.transactions_last_24h,
        "avg_transaction_amount": transaction.avg_transaction_amount,
        "failed_attempts": transaction.failed_attempts,
        "device_changed": transaction.device_changed,
        "location_changed": transaction.location_changed,
        "ip_risk_score": transaction.ip_risk_score,
        "previous_chargebacks": transaction.previous_chargebacks,
        "transaction_hour": transaction.transaction_hour,
        "payment_method": transaction.payment_method
    }

    risk_result = {
        "risk_score": transaction.risk_score,
        "risk_level": transaction.risk_level,
        "recommended_action": transaction.recommended_action,
        "reasons": reasons
    }

    investigation = investigate_transaction(
        transaction_data,
        risk_result
    )

    return {
        "success": True,
        "transaction_id": transaction.id,
        "investigation": investigation
    }

# --------------------------------------------------
# Model performance report
# --------------------------------------------------

@app.get(
    "/api/v1/reports/model-performance"
)
def model_performance_report():

    try:

        metrics = get_model_metrics()

        return {
            "success": True,
            "data": metrics
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to load model metrics"
        )

# --------------------------------------------------
# Customers
# --------------------------------------------------

@app.post("/api/v1/customers")
def create_customer(
    customer: CustomerRequest,
    db: Session = Depends(get_db)
):

    existing_customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id ==
            customer.customer_id
        )
        .first()
    )

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="Customer already exists"
        )

    new_customer = Customer(
        customer_id=customer.customer_id,
        name=customer.name,
        email=customer.email,
        account_age_days=customer.account_age_days
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "success": True,
        "data": {
            "id": new_customer.id,
            "customer_id":
                new_customer.customer_id,
            "name": new_customer.name,
            "email": new_customer.email,
            "account_age_days":
                new_customer.account_age_days
        }
    }


# --------------------------------------------------
# New Transaction with Customer Workflow
# --------------------------------------------------

@app.post("/api/v1/transactions/new")
def create_new_transaction(
    payload: NewTransactionRequest,
    db: Session = Depends(get_db)
):
    try:
        # -----------------------------------------
        # Find or create customer
        # -----------------------------------------

        customer = (
            db.query(Customer)
            .filter(
                Customer.customer_id ==
                payload.customer.customer_id
            )
            .first()
        )

        if not customer:

            customer = Customer(
                customer_id=
                    payload.customer.customer_id,

                name=
                    payload.customer.name,

                email=
                    payload.customer.email,

                account_age_days=
                    payload.customer.account_age_days
            )

            db.add(customer)
            db.flush()
            
        # -----------------------------------------
        # Get customer history
        # -----------------------------------------
        history = get_customer_history(customer.id, db)

        # -----------------------------------------
        # Prepare transaction data
        # -----------------------------------------

        transaction_data = {
            "amount": payload.amount,

            "account_age_days":
                payload.customer.account_age_days,

            "transactions_last_24h":
                payload.transactions_last_24h,

            "avg_transaction_amount":
                payload.avg_transaction_amount,

            "failed_attempts":
                payload.failed_attempts,

            "device_changed":
                payload.device_changed,

            "location_changed":
                payload.location_changed,

            "ip_risk_score":
                payload.ip_risk_score,

            "previous_chargebacks":
                payload.previous_chargebacks,

            "transaction_hour":
                payload.transaction_hour,

            "payment_method":
                payload.payment_method
        }

        transaction_data.update(history)

        # -----------------------------------------
        # Run RiskSentinel
        # -----------------------------------------

        result = assess_risk(
            transaction_data
        )

        # -----------------------------------------
        # Save transaction
        # -----------------------------------------

        new_transaction = Transaction(
            customer_id=customer.id,

            amount=payload.amount,

            account_age_days=
                payload.customer.account_age_days,

            transactions_last_24h=
                payload.transactions_last_24h,

            avg_transaction_amount=
                payload.avg_transaction_amount,

            failed_attempts=
                payload.failed_attempts,

            device_changed=
                payload.device_changed,

            location_changed=
                payload.location_changed,

            ip_risk_score=
                payload.ip_risk_score,

            previous_chargebacks=
                payload.previous_chargebacks,

            transaction_hour=
                payload.transaction_hour,

            payment_method=
                payload.payment_method,

            risk_score=
                result["risk_score"],

            risk_level=
                result["risk_level"],

            recommended_action=
                result["recommended_action"],

            risk_reasons="||".join(
                result["risk_reasons"]
            )
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return {
            "success": True,

            "customer": {
                "id": customer.id,
                "customer_id":
                    customer.customer_id,
                "name":
                    customer.name
            },

            "customer_history": history,

            "transaction": {
                "id": new_transaction.id,
                "risk_score":
                    new_transaction.risk_score,
                "risk_level":
                    new_transaction.risk_level,
                "recommended_action":
                    new_transaction.recommended_action,
                "reasons":
                    result["risk_reasons"]
            }
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unable to create transaction: {str(e)}"
        )

@app.get(
    "/api/v1/customers/{customer_id}"
)
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.customer_id ==
            customer_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    history = get_customer_history(
        customer.id,
        db
    )

    return {
        "success": True,

        "customer": {
            "id": customer.id,
            "customer_id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "account_age_days":
                customer.account_age_days,
        },

        "history": history,
    }
