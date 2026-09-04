import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier


# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "transactions.csv",
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml",
    "saved_models",
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "xgboost_risk_model.pkl",
)


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

# Make sure timestamp is parsed
df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

# Sort chronologically
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

    # Customer history features
    "previous_transaction_count",
    "historical_average_amount",
    "amount_vs_historical_average",
    "previous_high_risk_count",
    "previous_blocked_count",
    "transactions_last_1h",
]

target_column = "fraud_label"


X = df[feature_columns]
y = df[target_column]


# -----------------------------
# Chronological train/test split
# -----------------------------
split_index = int(len(df) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\nDataset information")
print("-------------------")
print(f"Total samples : {len(df):,}")
print(f"Training      : {len(X_train):,}")
print(f"Testing       : {len(X_test):,}")
print(f"Features      : {len(feature_columns)}")


# -----------------------------
# Preprocessing
# -----------------------------
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
    "transaction_hour",

    "previous_transaction_count",
    "historical_average_amount",
    "amount_vs_historical_average",
    "previous_high_risk_count",
    "previous_blocked_count",
    "transactions_last_1h",
]

categorical_features = [
    "payment_method"
]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            "passthrough",
            numeric_features,
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features,
        ),
    ]
)


# -----------------------------
# Transform data
# -----------------------------
X_train_processed = preprocessor.fit_transform(
    X_train
)

X_test_processed = preprocessor.transform(
    X_test
)


# -----------------------------
# XGBoost model
# -----------------------------
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1,
)


print("\nTraining XGBoost...")
print("-------------------")

model.fit(
    X_train_processed,
    y_train,
)


# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(
    X_test_processed
)

y_probability = model.predict_proba(
    X_test_processed
)[:, 1]


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

cm = confusion_matrix(
    y_test,
    y_pred,
)

tn, fp, fn, tp = cm.ravel()


# -----------------------------
# Print results
# -----------------------------
print("\nModel Performance")
print("-----------------")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

print("\nConfusion Matrix")
print("----------------")
print(cm)

print("\nDetailed Classification Report")
print("--------------------------------")
print(
    classification_report(
        y_test,
        y_pred,
        digits=4,
        zero_division=0,
    )
)


# -----------------------------
# Feature importance
# -----------------------------
feature_names = (
    numeric_features
    + list(
        preprocessor
        .named_transformers_["cat"]
        .get_feature_names_out(
            categorical_features
        )
    )
)

importance = pd.DataFrame(
    {
        "feature": feature_names,
        "importance": model.feature_importances_,
    }
).sort_values(
    "importance",
    ascending=False,
)

print("\nTop 15 Important Features")
print("-------------------------")
print(
    importance.head(15).to_string(
        index=False
    )
)


# -----------------------------
# Save model + preprocessor
# -----------------------------
os.makedirs(
    MODEL_DIR,
    exist_ok=True,
)

model_package = {
    "model": model,
    "preprocessor": preprocessor,
    "features": feature_columns,
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
}

joblib.dump(
    model_package,
    MODEL_PATH,
)


print(
    f"\nModel saved to: {MODEL_PATH}"
)
