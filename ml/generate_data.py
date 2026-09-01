import os
import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------
N_TRANSACTIONS = 50_000
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


def generate_transactions(n: int = N_TRANSACTIONS) -> pd.DataFrame:
    """Generate synthetic payment transaction data."""

    # -----------------------------
    # Basic transaction information
    # -----------------------------
    transaction_id = [f"TXN{i:06d}" for i in range(1, n + 1)]

    amount = np.round(
        np.random.lognormal(mean=6.0, sigma=1.0, size=n),
        2
    )

    account_age_days = np.random.randint(1, 2000, size=n)

    transactions_last_24h = np.random.poisson(
        lam=2.5,
        size=n
    )

    avg_transaction_amount = np.round(
        np.random.lognormal(mean=5.8, sigma=0.7, size=n),
        2
    )

    failed_attempts = np.random.poisson(
        lam=0.4,
        size=n
    )

    device_changed = np.random.binomial(
        n=1,
        p=0.08,
        size=n
    )

    location_changed = np.random.binomial(
        n=1,
        p=0.06,
        size=n
    )

    ip_risk_score = np.round(
        np.random.beta(2, 8, size=n),
        3
    )

    previous_chargebacks = np.random.poisson(
        lam=0.08,
        size=n
    )

    transaction_hour = np.random.randint(
        0,
        24,
        size=n
    )

    payment_method = np.random.choice(
        ["UPI", "CARD", "NETBANKING", "WALLET"],
        size=n,
        p=[0.45, 0.35, 0.10, 0.10]
    )

    # -----------------------------
    # Create a fraud-risk signal
    # -----------------------------
    risk_signal = np.zeros(n)

    # High transaction amount compared with user's normal amount
    amount_ratio = amount / (avg_transaction_amount + 1)

    risk_signal += np.where(
        amount_ratio > 5,
        2.5,
        0
    )

    risk_signal += np.where(
        amount_ratio > 10,
        1.5,
        0
    )

    # Very new accounts
    risk_signal += np.where(
        account_age_days < 30,
        2.0,
        0
    )

    # Many transactions in a short period
    risk_signal += np.where(
        transactions_last_24h >= 8,
        1.8,
        0
    )

    # Failed attempts
    risk_signal += failed_attempts * 0.7

    # New device
    risk_signal += device_changed * 1.5

    # New location
    risk_signal += location_changed * 1.2

    # Risky IP
    risk_signal += ip_risk_score * 4

    # Previous chargebacks
    risk_signal += previous_chargebacks * 1.5

    # Unusual late-night activity
    late_night = ((transaction_hour >= 0) &
                  (transaction_hour <= 4))
    risk_signal += late_night * 0.6

    # -----------------------------
    # Add randomness
    # -----------------------------
    risk_signal += np.random.normal(
        loc=0,
        scale=1.0,
        size=n
    )

    # -----------------------------
    # Convert signal to probability
    # -----------------------------
    fraud_probability = 1 / (
        1 + np.exp(-(risk_signal - 4.5))
    )

    # -----------------------------
    # Generate fraud label
    # -----------------------------
    fraud_label = np.random.binomial(
        1,
        fraud_probability
    )

    # -----------------------------
    # Create DataFrame
    # -----------------------------
    df = pd.DataFrame({
        "transaction_id": transaction_id,
        "amount": amount,
        "account_age_days": account_age_days,
        "transactions_last_24h": transactions_last_24h,
        "avg_transaction_amount": avg_transaction_amount,
        "failed_attempts": failed_attempts,
        "device_changed": device_changed,
        "location_changed": location_changed,
        "ip_risk_score": ip_risk_score,
        "previous_chargebacks": previous_chargebacks,
        "transaction_hour": transaction_hour,
        "payment_method": payment_method,
        "fraud_label": fraud_label,
    })

    return df


def main() -> None:
    df = generate_transactions()

    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data"
    )

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(
        output_dir,
        "transactions.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print("\nDataset generated successfully!")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Saved to: {output_path}")

    print("\nFraud distribution:")
    print(df["fraud_label"].value_counts())

    print("\nFraud percentage:")
    print(
        f"{df['fraud_label'].mean() * 100:.2f}%"
    )

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()
