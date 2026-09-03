from services.ai_investigator import investigate_transaction


transaction = {
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


risk_result = {
    "risk_score": 91,
    "risk_level": "HIGH",
    "recommended_action": "MANUAL_REVIEW",
    "reasons": [
        "Customer account is very new",
        "Multiple failed payment attempts detected",
        "New device detected",
        "High-risk IP signal"
    ]
}


result = investigate_transaction(
    transaction,
    risk_result
)

print("\n")
print(result)
