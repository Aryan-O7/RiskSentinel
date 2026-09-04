import os
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "transactions.csv",
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "xgboost_risk_model.pkl",
)


# Business costs
COST_PER_FALSE_POSITIVE = 500
COST_PER_FALSE_NEGATIVE = 2000


# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(DATA_PATH)

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

df = df.sort_values(
    "timestamp"
).reset_index(drop=True)


# -----------------------------
# Features
# -----------------------------
feature_columns = [
    "amount",
    "account_age_days",
    "transactions_last_24h",
    "avg_transaction_amount",
    "failed_attempts",
    "device_changed",
    "location_changed",
    "ip_risk_score",
    "previous_chargebacks",
    "transaction_hour",
    "payment_method",
    "previous_transaction_count",
    "historical_average_amount",
    "amount_vs_historical_average",
    "previous_high_risk_count",
    "previous_blocked_count",
    "transactions_last_1h",
]


# -----------------------------
# Chronological test set
# -----------------------------
split_index = int(len(df) * 0.80)

test_df = df.iloc[split_index:].copy()

X_test = test_df[feature_columns]
y_test = test_df["fraud_label"]


# -----------------------------
# Load model package
# -----------------------------
package = joblib.load(MODEL_PATH)

model = package["model"]
preprocessor = package["preprocessor"]


X_test_processed = preprocessor.transform(
    X_test
)


# -----------------------------
# Probabilities
# -----------------------------
y_probability = model.predict_proba(
    X_test_processed
)[:, 1]


# -----------------------------
# Threshold analysis
# -----------------------------
thresholds = np.arange(
    0.10,
    0.91,
    0.05,
)

results = []


for threshold in thresholds:

    y_pred = (
        y_probability >= threshold
    ).astype(int)

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        y_pred,
    ).ravel()

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    false_positive_cost = (
        fp * COST_PER_FALSE_POSITIVE
    )

    false_negative_cost = (
        fn * COST_PER_FALSE_NEGATIVE
    )

    total_cost = (
        false_positive_cost
        + false_negative_cost
    )

    results.append(
        {
            "threshold": round(
                float(threshold),
                2,
            ),
            "precision": round(
                precision,
                4,
            ),
            "recall": round(
                recall,
                4,
            ),
            "f1_score": round(
                f1,
                4,
            ),
            "true_negatives": tn,
            "false_positives": fp,
            "false_negatives": fn,
            "true_positives": tp,
            "false_positive_cost": false_positive_cost,
            "false_negative_cost": false_negative_cost,
            "total_cost": total_cost,
        }
    )


results_df = pd.DataFrame(results)


# -----------------------------
# Save results
# -----------------------------
output_path = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "threshold_results_v2.csv",
)

results_df.to_csv(
    output_path,
    index=False,
)


# -----------------------------
# Display results
# -----------------------------
print("\nThreshold Analysis")
print("==================")

print(
    results_df[
        [
            "threshold",
            "precision",
            "recall",
            "f1_score",
            "false_positives",
            "false_negatives",
            "total_cost",
        ]
    ].to_string(index=False)
)


# -----------------------------
# Best thresholds
# -----------------------------
best_cost = results_df.loc[
    results_df["total_cost"].idxmin()
]

best_f1 = results_df.loc[
    results_df["f1_score"].idxmax()
]

best_recall = results_df.loc[
    results_df["recall"].idxmax()
]


print("\nBest Threshold by Business Cost")
print("--------------------------------")
print(best_cost.to_string())


print("\nBest Threshold by F1")
print("--------------------")
print(best_f1.to_string())


print("\nBest Threshold by Recall")
print("------------------------")
print(best_recall.to_string())


print(
    f"\nResults saved to: {output_path}"
)
