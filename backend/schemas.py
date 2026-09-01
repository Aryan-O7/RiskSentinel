from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    amount: float = Field(gt=0)

    account_age_days: int = Field(
        ge=1
    )

    transactions_last_24h: int = Field(
        ge=0
    )

    avg_transaction_amount: float = Field(
        gt=0
    )

    failed_attempts: int = Field(
        ge=0
    )

    device_changed: int = Field(
        ge=0,
        le=1
    )

    location_changed: int = Field(
        ge=0,
        le=1
    )

    ip_risk_score: float = Field(
        ge=0,
        le=1
    )

    previous_chargebacks: int = Field(
        ge=0
    )

    transaction_hour: int = Field(
        ge=0,
        le=23
    )

    payment_method: str
