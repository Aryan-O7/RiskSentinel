import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/transactions.csv")

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
print(df.columns.tolist())


# -----------------------------
# Missing values
# -----------------------------
print("\n" + "=" * 50)
print("MISSING VALUES")
print("=" * 50)

print(df.isnull().sum())


# -----------------------------
# Fraud distribution
# -----------------------------
print("\n" + "=" * 50)
print("FRAUD DISTRIBUTION")
print("=" * 50)

fraud_counts = df["fraud_label"].value_counts()
print(fraud_counts)

print("\nPercentage:")
print(
    (df["fraud_label"].value_counts(normalize=True) * 100)
    .round(2)
)


# -----------------------------
# Basic statistics
# -----------------------------
print("\n" + "=" * 50)
print("NUMERICAL STATISTICS")
print("=" * 50)

print(df.describe().round(2))


# -----------------------------
# Compare legitimate vs fraud
# -----------------------------
print("\n" + "=" * 50)
print("LEGITIMATE VS FRAUD")
print("=" * 50)

comparison = df.groupby("fraud_label")[
    [
        "amount",
        "account_age_days",
        "transactions_last_24h",
        "avg_transaction_amount",
        "failed_attempts",
        "device_changed",
        "location_changed",
        "ip_risk_score",
        "previous_chargebacks"
    ]
].mean()

print(comparison.round(2))


# -----------------------------
# Transaction amount
# -----------------------------
plt.figure(figsize=(8, 5))

plt.hist(
    df[df["fraud_label"] == 0]["amount"],
    bins=50,
    alpha=0.6,
    label="Legitimate"
)

plt.hist(
    df[df["fraud_label"] == 1]["amount"],
    bins=50,
    alpha=0.6,
    label="Fraud"
)

plt.xlabel("Transaction Amount")
plt.ylabel("Number of Transactions")
plt.title("Transaction Amount Distribution")
plt.legend()
plt.savefig("data/chart_amount_distribution.png", dpi=100, bbox_inches="tight")
plt.close()
print("\nChart saved: data/chart_amount_distribution.png")


# -----------------------------
# Failed attempts
# -----------------------------
plt.figure(figsize=(8, 5))

df.groupby("failed_attempts")["fraud_label"].mean().plot(
    kind="bar"
)

plt.xlabel("Failed Attempts")
plt.ylabel("Fraud Rate")
plt.title("Fraud Rate by Failed Payment Attempts")
plt.tight_layout()
plt.savefig("data/chart_failed_attempts.png", dpi=100, bbox_inches="tight")
plt.close()
print("Chart saved: data/chart_failed_attempts.png")


# -----------------------------
# Device change
# -----------------------------
print("\n" + "=" * 50)
print("FRAUD RATE: DEVICE CHANGE")
print("=" * 50)

device_fraud = df.groupby("device_changed")["fraud_label"].mean() * 100
print(device_fraud.round(2))


# -----------------------------
# Location change
# -----------------------------
print("\n" + "=" * 50)
print("FRAUD RATE: LOCATION CHANGE")
print("=" * 50)

location_fraud = df.groupby("location_changed")["fraud_label"].mean() * 100
print(location_fraud.round(2))


# -----------------------------
# IP risk
# -----------------------------
print("\n" + "=" * 50)
print("AVERAGE IP RISK")
print("=" * 50)

print(
    df.groupby("fraud_label")["ip_risk_score"]
    .mean()
    .round(3)
)


# -----------------------------
# Correlation with fraud label
# -----------------------------
print("\n" + "=" * 50)
print("FEATURE CORRELATION WITH FRAUD")
print("=" * 50)

numeric_df = df.select_dtypes(include="number")

correlations = (
    numeric_df.corr()["fraud_label"]
    .drop("fraud_label")
    .sort_values(ascending=False)
)

print(correlations.round(3))

print("\nAnalysis completed.")
