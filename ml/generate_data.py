import os
from collections import defaultdict, deque

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------
N_TRANSACTIONS = 50_000
N_CUSTOMERS = 5_000
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)


def generate_transactions(
    n: int = N_TRANSACTIONS,
    n_customers: int = N_CUSTOMERS,
) -> pd.DataFrame:
    """Generate synthetic payment transactions with customer history."""

    # -----------------------------
    # Customer IDs
    # -----------------------------
    customer_ids = [
        f"CUST{i:05d}" for i in range(1, n_customers + 1)
    ]

    # Assign each transaction to a customer
    transaction_customer_ids = np.random.choice(
        customer_ids,
        size=n,
    )

    # -----------------------------
    # Timestamps
    # -----------------------------
    start_date = pd.Timestamp("2026-01-01")

    timestamps = pd.date_range(
        start=start_date,
        periods=n,
        freq="15min",
    )

    # Shuffle timestamps so customer activity is not tied
    # to transaction ID ordering.
    timestamps = np.array(timestamps)
    np.random.shuffle(timestamps)

    # -----------------------------
    # Basic transaction information
    # -----------------------------
    transaction_id = [
        f"TXN{i:06d}" for i in range(1, n + 1)
    ]

    amount = np.round(
        np.random.lognormal(
            mean=6.0,
            sigma=1.0,
            size=n,
        ),
        2,
    )

    account_age_days = np.random.randint(
        1,
        2000,
        size=n,
    )

    transactions_last_24h = np.random.poisson(
        lam=2.5,
        size=n,
    )

    avg_transaction_amount = np.round(
        np.random.lognormal(
            mean=5.8,
            sigma=0.7,
            size=n,
        ),
        2,
    )

    failed_attempts = np.random.poisson(
        lam=0.4,
        size=n,
    )

    device_changed = np.random.binomial(
        n=1,
        p=0.08,
        size=n,
    )

    location_changed = np.random.binomial(
        n=1,
        p=0.06,
        size=n,
    )

    ip_risk_score = np.round(
        np.random.beta(2, 8, size=n),
        3,
    )

    previous_chargebacks = np.random.poisson(
        lam=0.08,
        size=n,
    )

    transaction_hour = np.random.randint(
        0,
        24,
        size=n,
    )

    payment_method = np.random.choice(
        ["UPI", "CARD", "NETBANKING", "WALLET"],
        size=n,
        p=[0.45, 0.35, 0.10, 0.10],
    )

    # -----------------------------
    # Sort transactions chronologically
    # -----------------------------
    df = pd.DataFrame(
        {
            "transaction_id": transaction_id,
            "customer_id": transaction_customer_ids,
            "timestamp": timestamps,
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
        }
    )

    df = df.sort_values("timestamp").reset_index(drop=True)

    # -----------------------------
    # Customer history containers
    # -----------------------------
    customer_amounts = defaultdict(list)
    customer_high_risk = defaultdict(int)
    customer_blocked = defaultdict(int)

    # Store timestamps for recent activity
    customer_recent_transactions = defaultdict(deque)

    # -----------------------------
    # History features
    # -----------------------------
    previous_transaction_count = []
    historical_average_amount = []
    amount_vs_historical_average = []
    previous_high_risk_count = []
    previous_blocked_count = []
    transactions_last_1h = []

    for _, row in df.iterrows():

        customer_id = row["customer_id"]
        current_time = row["timestamp"]
        current_amount = row["amount"]

        # ---------------------------------
        # Remove transactions older than 1h
        # ---------------------------------
        recent_queue = customer_recent_transactions[
            customer_id
        ]

        while recent_queue:
            oldest_time = recent_queue[0]

            if current_time - oldest_time > pd.Timedelta(hours=1):
                recent_queue.popleft()
            else:
                break

        # ---------------------------------
        # Previous transaction count
        # ---------------------------------
        previous_count = len(
            customer_amounts[customer_id]
        )

        previous_transaction_count.append(
            previous_count
        )

        # ---------------------------------
        # Historical average amount
        # ---------------------------------
        if previous_count > 0:
            historical_avg = float(
                np.mean(customer_amounts[customer_id])
            )
        else:
            # For first transaction use current
            # baseline estimate.
            historical_avg = float(
                row["avg_transaction_amount"]
            )

        historical_average_amount.append(
            round(historical_avg, 2)
        )

        # ---------------------------------
        # Amount vs historical average
        # ---------------------------------
        amount_ratio = (
            current_amount /
            (historical_avg + 1)
        )

        amount_vs_historical_average.append(
            round(amount_ratio, 3)
        )

        # ---------------------------------
        # Previous risky transactions
        # ---------------------------------
        previous_high_risk_count.append(
            customer_high_risk[customer_id]
        )

        previous_blocked_count.append(
            customer_blocked[customer_id]
        )

        # ---------------------------------
        # Recent transaction velocity
        # ---------------------------------
        transactions_last_1h.append(
            len(recent_queue)
        )

        # ---------------------------------
        # Add CURRENT transaction to history
        # ---------------------------------
        customer_amounts[customer_id].append(
            current_amount
        )

        recent_queue.append(current_time)

        # Risk estimate used only to build
        # historical behavior for future rows.
        temporary_risk = 0

        if amount_ratio > 5:
            temporary_risk += 2.5

        if amount_ratio > 10:
            temporary_risk += 1.5

        if row["account_age_days"] < 30:
            temporary_risk += 2.0

        if row["transactions_last_24h"] >= 8:
            temporary_risk += 1.8

        temporary_risk += row["failed_attempts"] * 0.7
        temporary_risk += row["device_changed"] * 1.5
        temporary_risk += row["location_changed"] * 1.2
        temporary_risk += row["ip_risk_score"] * 4
        temporary_risk += row["previous_chargebacks"] * 1.5

        late_night = (
            row["transaction_hour"] >= 0
            and row["transaction_hour"] <= 4
        )

        temporary_risk += late_night * 0.6

        if temporary_risk >= 7:
            customer_high_risk[customer_id] += 1

        if temporary_risk >= 9:
            customer_blocked[customer_id] += 1

    # -----------------------------
    # Add history columns
    # -----------------------------
    df["previous_transaction_count"] = (
        previous_transaction_count
    )

    df["historical_average_amount"] = (
        historical_average_amount
    )

    df["amount_vs_historical_average"] = (
        amount_vs_historical_average
    )

    df["previous_high_risk_count"] = (
        previous_high_risk_count
    )

    df["previous_blocked_count"] = (
        previous_blocked_count
    )

    df["transactions_last_1h"] = (
        transactions_last_1h
    )

    # -----------------------------
    # Create fraud-risk signal
    # -----------------------------
    risk_signal = np.zeros(len(df))

    # Amount significantly above historical behavior
    risk_signal += np.where(
        df["amount_vs_historical_average"] > 5,
        2.5,
        0,
    )

    risk_signal += np.where(
        df["amount_vs_historical_average"] > 10,
        1.5,
        0,
    )

    # New accounts
    risk_signal += np.where(
        df["account_age_days"] < 30,
        2.0,
        0,
    )

    # High transaction velocity
    risk_signal += np.where(
        df["transactions_last_24h"] >= 8,
        1.8,
        0,
    )

    risk_signal += np.where(
        df["transactions_last_1h"] >= 3,
        1.5,
        0,
    )

    # Failed attempts
    risk_signal += (
        df["failed_attempts"] * 0.7
    )

    # Device change
    risk_signal += (
        df["device_changed"] * 1.5
    )

    # Location change
    risk_signal += (
        df["location_changed"] * 1.2
    )

    # Risky IP
    risk_signal += (
        df["ip_risk_score"] * 4
    )

    # Previous chargebacks
    risk_signal += (
        df["previous_chargebacks"] * 1.5
    )

    # Historical risky behavior
    risk_signal += np.where(
        df["previous_high_risk_count"] >= 2,
        1.5,
        0,
    )

    risk_signal += np.where(
        df["previous_blocked_count"] >= 1,
        2.0,
        0,
    )

    # Unusual late-night activity
    late_night = (
        (df["transaction_hour"] >= 0)
        & (df["transaction_hour"] <= 4)
    )

    risk_signal += (
        late_night.astype(int) * 0.6
    )

    # Randomness
    risk_signal += np.random.normal(
        loc=0,
        scale=1.0,
        size=len(df),
    )

    # -----------------------------
    # Probability
    # -----------------------------
    fraud_probability = 1 / (
        1
        + np.exp(
            -(risk_signal - 4.5)
        )
    )

    # -----------------------------
    # Fraud label
    # -----------------------------
    df["fraud_label"] = np.random.binomial(
        1,
        fraud_probability,
    )

    # -----------------------------
    # Sort by transaction ID
    # -----------------------------
    df = df.sort_values(
        "transaction_id"
    ).reset_index(drop=True)

    return df


def main() -> None:
    df = generate_transactions()

    output_dir = os.path.join(
        os.path.dirname(
            os.path.dirname(__file__)
        ),
        "data",
    )

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    output_path = os.path.join(
        output_dir,
        "transactions.csv",
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print("\nDataset generated successfully!")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Saved to: {output_path}")

    print("\nFraud distribution:")
    print(
        df["fraud_label"].value_counts()
    )

    print("\nFraud percentage:")
    print(
        f"{df['fraud_label'].mean() * 100:.2f}%"
    )

    print("\nCustomers:")
    print(
        df["customer_id"].nunique()
    )

    print("\nHistory features:")
    history_columns = [
        "previous_transaction_count",
        "historical_average_amount",
        "amount_vs_historical_average",
        "previous_high_risk_count",
        "previous_blocked_count",
        "transactions_last_1h",
    ]

    print(
        df[history_columns].describe()
    )

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()
