from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from datetime import datetime

from database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float, nullable=False)
    account_age_days = Column(Integer, nullable=False)
    transactions_last_24h = Column(Integer, nullable=False)
    avg_transaction_amount = Column(Float, nullable=False)
    failed_attempts = Column(Integer, nullable=False)

    device_changed = Column(Integer, nullable=False)
    location_changed = Column(Integer, nullable=False)

    ip_risk_score = Column(Float, nullable=False)
    previous_chargebacks = Column(Integer, nullable=False)

    transaction_hour = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False)

    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    recommended_action = Column(String, nullable=False)

    risk_reasons = Column(Text, nullable=True)

    review_decision = Column(
        String,
        nullable=True
    )

    reviewed_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
