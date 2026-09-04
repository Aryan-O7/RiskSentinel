import os
import joblib
import numpy as np


# -----------------------------
# Load model
# -----------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "xgboost_risk_model.pkl",
)

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
preprocessor = model_package["preprocessor"]
feature_columns = model_package["features"]


# -----------------------------
# Production threshold
# -----------------------------
THRESHOLD = 0.30


# -----------------------------
# Risk classification
# -----------------------------
def classify_risk(probability: float):
    """
    Convert fraud probability into application risk levels.
    """

    # Probability → 0–100 risk score
    risk_score = round(
        probability * 100,
        2,
    )

    if probability < 0.30:
        risk_level = "LOW"
        recommended_action = "ALLOW"

    elif probability < 0.70:
        risk_level = "MEDIUM"
        recommended_action = "MONITOR"

    else:
        risk_level = "HIGH"
        recommended_action = "MANUAL_REVIEW"

    return (
        risk_score,
        risk_level,
        recommended_action,
    )


# -----------------------------
# Build reasons
# -----------------------------
def generate_reasons(transaction: dict):
    reasons = []

    amount = transaction.get(
        "amount",
        0,
    )

    historical_average = transaction.get(
        "historical_average_amount",
        0,
    )

    amount_ratio = transaction.get(
        "amount_vs_historical_average",
        1,
    )

    if amount_ratio > 5:
        reasons.append(
            "Transaction amount is significantly above the customer's historical average."
        )

    if transaction.get(
        "device_changed",
        0,
    ):
        reasons.append(
            "Transaction was made from a new device."
        )

    if transaction.get(
        "location_changed",
        0,
    ):
        reasons.append(
            "Transaction location differs from previous activity."
        )

    if transaction.get(
        "failed_attempts",
        0,
    ) >= 3:
        reasons.append(
            "Multiple failed payment attempts detected."
        )

    if transaction.get(
        "ip_risk_score",
        0,
    ) >= 0.50:
        reasons.append(
            "IP address has elevated risk signals."
        )

    if transaction.get(
        "previous_chargebacks",
        0,
    ) > 0:
        reasons.append(
            "Customer has previous chargeback activity."
        )

    if transaction.get(
        "previous_high_risk_count",
        0,
    ) >= 2:
        reasons.append(
            "Customer has multiple previous high-risk transactions."
        )

    if transaction.get(
        "previous_blocked_count",
        0,
    ) > 0:
        reasons.append(
            "Customer has previously had a blocked transaction."
        )

    if transaction.get(
        "transactions_last_1h",
        0,
    ) >= 3:
        reasons.append(
            "Unusually high transaction velocity detected."
        )

    if not reasons:
        reasons.append(
            "No major risk indicators detected."
        )

    return reasons


# -----------------------------
# Main risk assessment
# -----------------------------
def assess_transaction(transaction: dict):
    """
    Assess a transaction using the history-aware XGBoost model.
    """

    # -------------------------
    # Safety defaults
    # -------------------------
    historical_average = transaction.get(
        "historical_average_amount",
        transaction.get(
            "avg_transaction_amount",
            0,
        ),
    )

    if historical_average <= 0:
        historical_average = transaction.get(
            "avg_transaction_amount",
            1,
        )

    amount = transaction.get(
        "amount",
        0,
    )

    amount_ratio = amount / (
        historical_average + 1
    )

    # -------------------------
    # Prepare model input
    # -------------------------
    model_input = {
        "amount": amount,
        "account_age_days": transaction.get(
            "account_age_days",
            0,
        ),
        "transactions_last_24h": transaction.get(
            "transactions_last_24h",
            0,
        ),
        "avg_transaction_amount": transaction.get(
            "avg_transaction_amount",
            historical_average,
        ),
        "failed_attempts": transaction.get(
            "failed_attempts",
            0,
        ),
        "device_changed": transaction.get(
            "device_changed",
            0,
        ),
        "location_changed": transaction.get(
            "location_changed",
            0,
        ),
        "ip_risk_score": transaction.get(
            "ip_risk_score",
            0,
        ),
        "previous_chargebacks": transaction.get(
            "previous_chargebacks",
            0,
        ),
        "transaction_hour": transaction.get(
            "transaction_hour",
            12,
        ),
        "payment_method": transaction.get(
            "payment_method",
            "UPI",
        ),

        # Customer history
        "previous_transaction_count": transaction.get(
            "previous_transaction_count",
            0,
        ),
        "historical_average_amount": historical_average,
        "amount_vs_historical_average": transaction.get(
            "amount_vs_historical_average",
            amount_ratio,
        ),
        "previous_high_risk_count": transaction.get(
            "previous_high_risk_count",
            0,
        ),
        "previous_blocked_count": transaction.get(
            "previous_blocked_count",
            0,
        ),
        "transactions_last_1h": transaction.get(
            "transactions_last_1h",
            0,
        ),
    }

    # -------------------------
    # Create DataFrame
    # -------------------------
    import pandas as pd

    input_df = pd.DataFrame(
        [model_input]
    )

    # Make sure column order exactly matches training
    input_df = input_df[
        feature_columns
    ]

    # -------------------------
    # Transform
    # -------------------------
    processed_input = (
        preprocessor.transform(
            input_df
        )
    )

    # -------------------------
    # Predict probability
    # -------------------------
    probability = float(
        model.predict_proba(
            processed_input
        )[0][1]
    )

    # -------------------------
    # Classification
    # -------------------------
    (
        risk_score,
        risk_level,
        recommended_action,
    ) = classify_risk(
        probability
    )

    # -------------------------
    # Reasons
    # -------------------------
    reasons = generate_reasons(
        model_input
    )

    return {
        "risk_score": risk_score,
        "risk_probability": round(
            probability,
            4,
        ),
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "risk_reasons": reasons,
        "model": "XGBoost",
        "model_version": "history-aware-v1",
    }


if __name__ == "__main__":
    test_transaction = {
        "amount": 15000,
        "account_age_days": 120,
        "transactions_last_24h": 5,
        "avg_transaction_amount": 800,
        "failed_attempts": 2,
        "device_changed": 1,
        "location_changed": 1,
        "ip_risk_score": 0.65,
        "previous_chargebacks": 1,
        "transaction_hour": 2,
        "payment_method": "CARD",

        "previous_transaction_count": 12,
        "historical_average_amount": 850,
        "amount_vs_historical_average": 17.63,
        "previous_high_risk_count": 3,
        "previous_blocked_count": 1,
        "transactions_last_1h": 3,
    }
    
    result = assess_transaction(test_transaction)
    print("\nRisk Assessment Result:")
    import json
    print(json.dumps(result, indent=2))
