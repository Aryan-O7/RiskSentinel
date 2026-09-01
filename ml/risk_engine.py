import os
import joblib
import pandas as pd


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "saved_models",
    "xgboost_risk_model.pkl"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# Risk thresholds (data-driven from threshold_analysis.py)
# Optimal cost threshold = 0.55, best F1 threshold = 0.65
# Rs.500/FP and Rs.2000/FN assumptions
# --------------------------------------------------

HIGH_RISK_THRESHOLD = 80   # probability >= 0.80 -> HIGH
MEDIUM_RISK_THRESHOLD = 55  # probability >= 0.55 -> MEDIUM, < 0.55 -> LOW


# --------------------------------------------------
# Risk classification
# --------------------------------------------------

def classify_risk(risk_score: int) -> str:
    """
    Convert a 0-100 risk score into a risk level.
    Thresholds selected via threshold_analysis.py
    to minimize total business cost.
    """

    if risk_score < MEDIUM_RISK_THRESHOLD:
        return "LOW"

    if risk_score < HIGH_RISK_THRESHOLD:
        return "MEDIUM"

    return "HIGH"


# --------------------------------------------------
# Recommended action
# --------------------------------------------------

def recommended_action(risk_level: str) -> str:
    """
    Decide what action should be taken.
    """

    if risk_level == "LOW":
        return "ALLOW"

    if risk_level == "MEDIUM":
        return "MONITOR"

    return "MANUAL_REVIEW"


# --------------------------------------------------
# Generate explanation
# --------------------------------------------------

def generate_reasons(transaction: dict) -> list[str]:
    """
    Generate simple rule-based explanations
    for why a transaction may be risky.
    """

    reasons = []

    amount = float(transaction["amount"])
    avg_amount = float(
        transaction["avg_transaction_amount"]
    )

    amount_ratio = amount / (avg_amount + 1)

    if amount_ratio > 5:
        reasons.append(
            "Transaction amount is unusually high "
            "compared with historical average"
        )

    if transaction["account_age_days"] < 30:
        reasons.append(
            "Customer account is very new"
        )

    if transaction["transactions_last_24h"] >= 8:
        reasons.append(
            "Unusually high transaction frequency"
        )

    if transaction["failed_attempts"] >= 3:
        reasons.append(
            "Multiple failed payment attempts detected"
        )

    if transaction["device_changed"] == 1:
        reasons.append(
            "New device detected"
        )

    if transaction["location_changed"] == 1:
        reasons.append(
            "Unusual location change detected"
        )

    if transaction["ip_risk_score"] >= 0.6:
        reasons.append(
            "High-risk IP signal"
        )

    if transaction["previous_chargebacks"] >= 1:
        reasons.append(
            "Previous chargeback history detected"
        )

    if transaction["transaction_hour"] <= 4:
        reasons.append(
            "Transaction occurred during unusual hours"
        )

    if not reasons:
        reasons.append(
            "No major individual risk signals detected"
        )

    return reasons


# --------------------------------------------------
# Risk prediction
# --------------------------------------------------

def assess_transaction(transaction: dict) -> dict:
    """
    Assess one payment transaction.
    """

    # Convert input into DataFrame
    transaction_df = pd.DataFrame([transaction])

    # Get fraud probability
    probability = model.predict_proba(
        transaction_df
    )[0][1]

    # Convert probability to 0-100
    risk_score = round(
        float(probability) * 100
    )

    # Make sure score is within range
    risk_score = max(
        0,
        min(100, risk_score)
    )

    # Classify risk
    risk_level = classify_risk(
        risk_score
    )

    # Decide action
    action = recommended_action(
        risk_level
    )

    # Generate reasons
    reasons = generate_reasons(
        transaction
    )

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommended_action": action,
        "reasons": reasons
    }


# --------------------------------------------------
# Test transactions
# --------------------------------------------------

def print_assessment(label: str, transaction: dict):
    result = assess_transaction(transaction)
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")
    print(f"  Risk Score : {result['risk_score']}/100")
    print(f"  Risk Level : {result['risk_level']}")
    print(f"  Action     : {result['recommended_action']}")
    print(f"\n  Risk Reasons:")
    for i, reason in enumerate(result["reasons"], start=1):
        print(f"    {i}. {reason}")


if __name__ == "__main__":

    # --- HIGH RISK ---
    high_risk = {
        "amount": 18500,
        "account_age_days": 3,
        "transactions_last_24h": 10,
        "avg_transaction_amount": 1200,
        "failed_attempts": 4,
        "device_changed": 1,
        "location_changed": 1,
        "ip_risk_score": 0.85,
        "previous_chargebacks": 1,
        "transaction_hour": 2,
        "payment_method": "UPI"
    }

    # --- LOW RISK ---
    low_risk = {
        "amount": 650,
        "account_age_days": 800,
        "transactions_last_24h": 2,
        "avg_transaction_amount": 700,
        "failed_attempts": 0,
        "device_changed": 0,
        "location_changed": 0,
        "ip_risk_score": 0.05,
        "previous_chargebacks": 0,
        "transaction_hour": 14,
        "payment_method": "UPI"
    }

    # --- MEDIUM RISK ---
    medium_risk = {
        "amount": 4500,
        "account_age_days": 120,
        "transactions_last_24h": 5,
        "avg_transaction_amount": 1500,
        "failed_attempts": 1,
        "device_changed": 0,
        "location_changed": 1,
        "ip_risk_score": 0.35,
        "previous_chargebacks": 0,
        "transaction_hour": 20,
        "payment_method": "CARD"
    }

    print("\nRISKSENTINEL TRANSACTION ASSESSMENTS")

    print_assessment("TEST 1 — HIGH RISK TRANSACTION", high_risk)
    print_assessment("TEST 2 — LOW RISK TRANSACTION", low_risk)
    print_assessment("TEST 3 — MEDIUM RISK TRANSACTION", medium_risk)
