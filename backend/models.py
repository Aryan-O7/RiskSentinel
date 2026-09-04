from sqlalchemy import Column, Integer, Float, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    account_age_days = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="customer")


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=True
    )

    customer = relationship(
        "Customer",
        back_populates="transactions"
    )

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
