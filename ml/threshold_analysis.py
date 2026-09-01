import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
# Load data — same split as training
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["transaction_id", "fraud_label"])
y = df["fraud_label"]

# Same split as train_xgboost.py
X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

model = joblib.load(MODEL_PATH)

probabilities = model.predict_proba(X_test)[:, 1]


# --------------------------------------------------
# Cost assumptions
# --------------------------------------------------

COST_PER_FALSE_POSITIVE = 500
COST_PER_FALSE_NEGATIVE = 2000


# --------------------------------------------------
# Analyze thresholds (finer granularity)
# --------------------------------------------------

results = []

for threshold in [
    0.05, 0.10, 0.15, 0.20, 0.25,
    0.30, 0.35, 0.40, 0.45, 0.50,
    0.55, 0.60, 0.65, 0.70, 0.75,
    0.80, 0.85, 0.90, 0.95
]:
    predictions = (probabilities >= threshold).astype(int)

    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()

    fp_cost = fp * COST_PER_FALSE_POSITIVE
    fn_cost = fn * COST_PER_FALSE_NEGATIVE
    total_cost = fp_cost + fn_cost

    results.append({
        "Threshold": threshold,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
        "FP": fp,
        "FN": fn,
        "FP_Cost": fp_cost,
        "FN_Cost": fn_cost,
        "Total_Cost": total_cost
    })


# --------------------------------------------------
# Display
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv("threshold_results.csv", index=False)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)

print("\n" + "=" * 130)
print("THRESHOLD ANALYSIS — OPTIMIZED XGBOOST")
print("=" * 130)

display_df = results_df.copy()
display_df["Precision"] = display_df["Precision"].round(4)
display_df["Recall"] = display_df["Recall"].round(4)
display_df["F1"] = display_df["F1"].round(4)
display_df["FP_Cost"] = display_df["FP_Cost"].apply(lambda x: f"Rs.{x:>10,.0f}")
display_df["FN_Cost"] = display_df["FN_Cost"].apply(lambda x: f"Rs.{x:>10,.0f}")
display_df["Total_Cost"] = display_df["Total_Cost"].apply(lambda x: f"Rs.{x:>10,.0f}")

print(display_df.to_string(index=False))


# --------------------------------------------------
# Best threshold by total cost
# --------------------------------------------------

best_idx = results_df["Total_Cost"].idxmin()
best = results_df.loc[best_idx]

# Also find best F1
best_f1_idx = results_df["F1"].idxmax()
best_f1 = results_df.loc[best_f1_idx]

print("\n" + "=" * 60)
print("BEST THRESHOLD — LOWEST TOTAL BUSINESS COST")
print("=" * 60)
print(f"  Threshold      : {best['Threshold']}")
print(f"  Precision      : {best['Precision']:.4f}")
print(f"  Recall         : {best['Recall']:.4f}")
print(f"  F1             : {best['F1']:.4f}")
print(f"  False Positives: {int(best['FP'])}")
print(f"  False Negatives: {int(best['FN'])}")
print(f"  Total Cost     : Rs.{best['Total_Cost']:,.0f}")

print("\n" + "=" * 60)
print("BEST THRESHOLD — HIGHEST F1 SCORE")
print("=" * 60)
print(f"  Threshold      : {best_f1['Threshold']}")
print(f"  Precision      : {best_f1['Precision']:.4f}")
print(f"  Recall         : {best_f1['Recall']:.4f}")
print(f"  F1             : {best_f1['F1']:.4f}")
print(f"  False Positives: {int(best_f1['FP'])}")
print(f"  False Negatives: {int(best_f1['FN'])}")
print(f"  Total Cost     : Rs.{best_f1['Total_Cost']:,.0f}")

print("\n" + "=" * 60)
print("RECOMMENDED RISK THRESHOLDS")
print("=" * 60)

# Find the threshold where precision is roughly 0.50 for MEDIUM boundary
# and where recall starts dropping significantly for HIGH boundary
medium_threshold = best["Threshold"]
high_candidates = results_df[results_df["Precision"] >= 0.60]
if not high_candidates.empty:
    high_threshold = high_candidates.iloc[0]["Threshold"]
else:
    high_threshold = 0.70

print(f"  LOW    : risk_score < {int(medium_threshold * 100)}")
print(f"  MEDIUM : {int(medium_threshold * 100)} <= risk_score < {int(high_threshold * 100)}")
print(f"  HIGH   : risk_score >= {int(high_threshold * 100)}")
print()
print("  Cost assumptions (prototype):")
print("    Rs.500 per False Positive")
print("    Rs.2,000 per False Negative")
