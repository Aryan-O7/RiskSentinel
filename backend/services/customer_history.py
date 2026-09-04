from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models import Customer, Transaction


def get_customer_history(
    customer_id: int,
    db: Session,
):
    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        return {
            "previous_transaction_count": 0,
            "historical_average_amount": 0,
            "previous_high_risk_count": 0,
            "previous_blocked_count": 0,
            "previous_review_count": 0,
            "previous_chargeback_count": 0,
            "transactions_last_1h": 0,
            "transactions_last_24h": 0,
        }

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.customer_id == customer.id
        )
        .order_by(
            Transaction.created_at.asc()
        )
        .all()
    )

    previous_count = len(transactions)

    if previous_count:
        historical_average = sum(
            float(t.amount)
            for t in transactions
        ) / previous_count
    else:
        historical_average = 0

    previous_high_risk_count = sum(
        1
        for t in transactions
        if t.risk_level == "HIGH"
    )

    previous_blocked_count = sum(
        1
        for t in transactions
        if t.review_decision == "BLOCK"
    )

    previous_review_count = sum(
        1
        for t in transactions
        if t.review_decision == "REVIEW"
    )

    previous_chargeback_count = sum(
        int(t.previous_chargebacks or 0)
        for t in transactions
    )

    now = datetime.utcnow()

    one_hour_ago = now - timedelta(hours=1)
    twenty_four_hours_ago = now - timedelta(hours=24)

    transactions_last_1h = sum(
        1
        for t in transactions
        if t.created_at
        and t.created_at >= one_hour_ago
    )

    transactions_last_24h = sum(
        1
        for t in transactions
        if t.created_at
        and t.created_at >= twenty_four_hours_ago
    )

    return {
        "previous_transaction_count": previous_count,
        "historical_average_amount": round(
            historical_average,
            2,
        ),
        "previous_high_risk_count": (
            previous_high_risk_count
        ),
        "previous_blocked_count": (
            previous_blocked_count
        ),
        "previous_review_count": (
            previous_review_count
        ),
        "previous_chargeback_count": (
            previous_chargeback_count
        ),
        "transactions_last_1h": transactions_last_1h,
        "transactions_last_24h": transactions_last_24h,
    }
