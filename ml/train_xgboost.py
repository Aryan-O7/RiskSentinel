import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)

from xgboost import XGBClassifier


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "transactions.csv"
)

MODEL_DIR = os.path.join(
    os.path.dirname(__file__),
    "saved_models"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print(f"Dataset: {df.shape[0]:,} rows")
print(f"Columns: {df.shape[1]}")


# --------------------------------------------------
# Features and target
# --------------------------------------------------

X = df.drop(
    columns=["transaction_id", "fraud_label"]
)

y = df["fraud_label"]


# --------------------------------------------------
# Feature types
# --------------------------------------------------

categorical_features = [
    "payment_method"
]

numeric_features = [
    "amount",
    "account_age_days",
    "transactions_last_24h",
    "avg_transaction_amount",
    "failed_attempts",
    "device_changed",
    "location_changed",
    "ip_risk_score",
    "previous_chargebacks",
    "transaction_hour"
]


# --------------------------------------------------
# Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# --------------------------------------------------
# Train / Val / Test split (70 / 15 / 15)
# --------------------------------------------------

X_train_full, X_test, y_train_full, y_test = train_test_split(
    X, y,
    test_size=0.15,
    random_state=42,
    stratify=y
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train_full, y_train_full,
    test_size=0.176,  # 0.176 of 85% ~ 15% of total
    random_state=42,
    stratify=y_train_full
)

print(f"\nTrain : {len(X_train):,}")
print(f"Val   : {len(X_val):,}")
print(f"Test  : {len(X_test):,}")

# Calculate class imbalance ratio for scale_pos_weight
neg_count = (y_train == 0).sum()
pos_count = (y_train == 1).sum()
scale_ratio = neg_count / pos_count

print(f"\nClass ratio (neg/pos): {scale_ratio:.2f}")
print(f"  Legit: {neg_count:,}  |  Fraud: {pos_count:,}")


# --------------------------------------------------
# Optimized XGBoost model
# --------------------------------------------------

model = XGBClassifier(
    n_estimators=500,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    scale_pos_weight=scale_ratio,   # Handle class imbalance
    objective="binary:logistic",
    eval_metric="auc",
    early_stopping_rounds=30,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# Pipeline
# --------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# --------------------------------------------------
# Train with early stopping on validation set
# --------------------------------------------------

print("\nTraining optimized XGBoost...")

# Pre-transform validation data for eval_set
X_val_transformed = preprocessor.fit_transform(X_train)  # fit on train
X_val_transformed = preprocessor.transform(X_val)

pipeline.fit(
    X_train,
    y_train,
    model__eval_set=[(X_val_transformed, y_val)],
    model__verbose=False
)

best_iteration = pipeline.named_steps["model"].best_iteration
print(f"Training completed. Best iteration: {best_iteration}")


# --------------------------------------------------
# Evaluate on TEST set
# --------------------------------------------------

y_pred = pipeline.predict(X_test)
y_probability = pipeline.predict_proba(X_test)[:, 1]


print("\n" + "=" * 60)
print("OPTIMIZED XGBOOST — TEST SET RESULTS")
print("=" * 60)

print(
    classification_report(
        y_test, y_pred, digits=4
    )
)


print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

cm = confusion_matrix(y_test, y_pred)
print(cm)

tn, fp, fn, tp = cm.ravel()
print(f"\n  TN={tn}  FP={fp}")
print(f"  FN={fn}  TP={tp}")


auc = roc_auc_score(y_test, y_probability)
print(f"\nROC-AUC: {auc:.4f}")


# --------------------------------------------------
# Save model
# --------------------------------------------------

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "xgboost_risk_model.pkl"
)

joblib.dump(pipeline, MODEL_PATH)

print(f"\nModel saved: {MODEL_PATH}")
