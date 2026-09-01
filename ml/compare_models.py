import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "transactions.csv")

LOGISTIC_PATH = os.path.join(
    os.path.dirname(__file__), "saved_models", "risk_model.pkl"
)

XGB_PATH = os.path.join(
    os.path.dirname(__file__), "saved_models", "xgboost_risk_model.pkl"
)


# -----------------------------------------
# Load data — use 15% test to match XGBoost training
# -----------------------------------------

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["transaction_id", "fraud_label"])
y = df["fraud_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)


# -----------------------------------------
# Load models
# -----------------------------------------

logistic_model = joblib.load(LOGISTIC_PATH)
xgb_model = joblib.load(XGB_PATH)

# Retrain Logistic Regression on same split for fair comparison
logistic_model.fit(X_train, y_train)

models = {
    "Logistic Regression": logistic_model,
    "XGBoost (Optimized)": xgb_model
}

results = []

for name, model in models.items():
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)
    roc_auc = roc_auc_score(y_test, probabilities)

    tn, fp, fn, tp = confusion_matrix(y_test, predictions).ravel()

    results.append({
        "Model": name,
        "Precision": round(precision, 4),
        "Recall": round(recall, 4),
        "F1": round(f1, 4),
        "ROC-AUC": round(roc_auc, 4),
        "FP": int(fp),
        "FN": int(fn)
    })


results_df = pd.DataFrame(results)

print("\n" + "=" * 90)
print("MODEL COMPARISON (same test set)")
print("=" * 90)
print(results_df.to_string(index=False))

# Business cost
COST_PER_FP = 500
COST_PER_FN = 2000

print("\n" + "=" * 90)
print("BUSINESS COST COMPARISON")
print("=" * 90)

for r in results:
    fp_cost = r["FP"] * COST_PER_FP
    fn_cost = r["FN"] * COST_PER_FN
    total = fp_cost + fn_cost
    print(f"  {r['Model']:25s}  FP={r['FP']:>5d} (Rs.{fp_cost:>10,.0f})   "
          f"FN={r['FN']:>5d} (Rs.{fn_cost:>10,.0f})   "
          f"Total=Rs.{total:>10,.0f}")
