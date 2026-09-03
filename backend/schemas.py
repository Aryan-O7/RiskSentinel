from typing import Literal
from pydantic import BaseModel, Field, model_validator

class TransactionRequest(BaseModel):
    amount: float = Field(gt=0)
    account_age_days: int = Field(ge=1)
    transactions_last_24h: int = Field(ge=0, le=1000)
    avg_transaction_amount: float = Field(gt=0)
    failed_attempts: int = Field(ge=0, le=100)
    device_changed: int = Field(ge=0, le=1)
    location_changed: int = Field(ge=0, le=1)
    ip_risk_score: float = Field(ge=0, le=1)
    previous_chargebacks: int = Field(ge=0, le=100)
    transaction_hour: int = Field(ge=0, le=23)
    payment_method: Literal["UPI", "CARD", "NETBANKING", "WALLET"]

    @model_validator(mode="after")
    def validate_amounts(self):
        if self.avg_transaction_amount > 10_000_000:
            raise ValueError("Average transaction amount is invalid.")
        return self
