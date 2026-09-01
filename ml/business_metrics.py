import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix


# -----------------------------------------
# Load data
# -----------------------------------------

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "transactions.csv"
)

df = pd.read_csv(DATA_PATH)


# -----------------------------------------
# Features / target
# -----------------------------------------

X = df.drop(
    columns=["transaction_id", "fraud_label"]
)

y = df["fraud_label"]


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


# -----------------------------------------
# Preprocessing
# -----------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            StandardScaler(),
            numeric_features
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# -----------------------------------------
# Split
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# -----------------------------------------
# Train
# -----------------------------------------

pipeline.fit(
    X_train,
    y_train
)


# -----------------------------------------
# Predict
# -----------------------------------------

y_pred = pipeline.predict(X_test)


# -----------------------------------------
# Confusion matrix
# -----------------------------------------

tn, fp, fn, tp = confusion_matrix(
    y_test,
    y_pred
).ravel()


# -----------------------------------------
# Business assumptions
# -----------------------------------------

COST_PER_FALSE_POSITIVE = 500

false_positive_cost = (
    fp * COST_PER_FALSE_POSITIVE
)


# -----------------------------------------
# Results
# -----------------------------------------

print("=" * 50)
print("BUSINESS RISK METRICS")
print("=" * 50)

print(f"True Negatives : {tn}")
print(f"False Positives: {fp}")
print(f"False Negatives: {fn}")
print(f"True Positives : {tp}")

print(
    f"\nEstimated False Positive Cost: "
    f"Rs.{false_positive_cost:,.2f}"
)
