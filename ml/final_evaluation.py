import json
import os

import joblib
import pandas as pd
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

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

METRICS_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
    "metrics.json",
)


# -----------------------------
# Production threshold
# -----------------------------
# Use the threshold selected from
# threshold_analysis_v2.py.
THRESHOLD = 0.30


# Business costs
COST_PER_FALSE_POSITIVE = 500
COST_PER_FALSE_NEGATIVE = 2000


# -----------------------------
# Load dataset
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
# Test split
# -----------------------------
split_index = int(
    len(df) * 0.80
)

test_df = df.iloc[
    split_index:
].copy()

X_test = test_df[
    feature_columns
]

y_test = test_df[
    "fraud_label"
]


# -----------------------------
# Load model
# -----------------------------
package = joblib.load(
    MODEL_PATH
)

model = package["model"]
preprocessor = package["preprocessor"]


X_test_processed = (
    preprocessor.transform(X_test)
)


# -----------------------------
# Predictions
# -----------------------------
y_probability = (
    model.predict_proba(
        X_test_processed
    )[:, 1]
)

y_pred = (
    y_probability >= THRESHOLD
).astype(int)


# -----------------------------
# Metrics
# -----------------------------
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

roc_auc = roc_auc_score(
    y_test,
    y_probability,
)

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred,
).ravel()


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


# -----------------------------
# Save metrics
# -----------------------------
metrics = {
    "model": "XGBoost",
    "model_version": "history-aware-v1",
    "threshold": THRESHOLD,
    "test_samples": len(test_df),

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

    "roc_auc": round(
        roc_auc,
        4,
    ),

    "true_negatives": int(tn),
    "false_positives": int(fp),
    "false_negatives": int(fn),
    "true_positives": int(tp),

    "false_positive_cost": int(
        false_positive_cost
    ),

    "false_negative_cost": int(
        false_negative_cost
    ),

    "total_estimated_cost": int(
        total_cost
    ),
}


with open(
    METRICS_PATH,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        metrics,
        f,
        indent=4,
    )


# -----------------------------
# Print final evaluation
# -----------------------------
print("\nFinal Model Evaluation")
print("======================")

print(
    f"Threshold : {THRESHOLD:.2f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)

print("\nConfusion Matrix")
print("----------------")
print(
    f"TN: {tn}"
)

print(
    f"FP: {fp}"
)

print(
    f"FN: {fn}"
)

print(
    f"TP: {tp}"
)

print("\nBusiness Cost")
print("-------------")

print(
    f"False Positive Cost : ₹{false_positive_cost:,}"
)

print(
    f"False Negative Cost : ₹{false_negative_cost:,}"
)

print(
    f"Total Estimated Cost: ₹{total_cost:,}"
)

print(
    f"\nMetrics saved to: {METRICS_PATH}"
)
