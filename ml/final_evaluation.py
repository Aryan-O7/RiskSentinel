import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "transactions.csv"
)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "saved_models",
    "xgboost_risk_model.pkl"
)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df.drop(
    columns=[
        "transaction_id",
        "fraud_label"
    ]
)

y = df["fraud_label"]


# --------------------------------------------------
# Final held-out test set
# --------------------------------------------------

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# Predictions
# --------------------------------------------------

probabilities = model.predict_proba(
    X_test
)[:, 1]

# Set THRESHOLD to 0.50 for evaluation
THRESHOLD = 0.50

predictions = (
    probabilities >= THRESHOLD
).astype(int)


# --------------------------------------------------
# Metrics
# --------------------------------------------------

precision = precision_score(
    y_test,
    predictions,
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)


# --------------------------------------------------
# Confusion matrix
# --------------------------------------------------

tn, fp, fn, tp = confusion_matrix(
    y_test,
    predictions
).ravel()


# --------------------------------------------------
# Business cost assumptions
# --------------------------------------------------

COST_PER_FALSE_POSITIVE = 500
COST_PER_FALSE_NEGATIVE = 2000

fp_cost = (
    fp * COST_PER_FALSE_POSITIVE
)

fn_cost = (
    fn * COST_PER_FALSE_NEGATIVE
)

total_cost = fp_cost + fn_cost


# --------------------------------------------------
# Print results
# --------------------------------------------------

print("\n" + "=" * 70)
print("RISKSENTINEL FINAL MODEL EVALUATION")
print("=" * 70)

print(f"\nTest samples: {len(y_test):,}")

print("\nClassification metrics")
print("-" * 40)

print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

print("\nConfusion Matrix")
print("-" * 40)

print(f"True Negatives : {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives : {tp}")

print("\nBusiness Cost")
print("-" * 40)

print(
    f"False-positive cost: Rs.{fp_cost:,.2f}"
)

print(
    f"False-negative cost: Rs.{fn_cost:,.2f}"
)

print(
    f"Total estimated cost: Rs.{total_cost:,.2f}"
)

print("\nDetailed Classification Report")
print("-" * 40)

print(
    classification_report(
        y_test,
        predictions,
        digits=4
    )
)
