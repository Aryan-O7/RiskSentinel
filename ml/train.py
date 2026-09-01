import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "transactions.csv"
)

df = pd.read_csv(DATA_PATH)

print("Dataset loaded")
print(f"Rows: {len(df):,}")


# --------------------------------------------------
# 2. Remove columns we don't want as features
# --------------------------------------------------

X = df.drop(
    columns=["transaction_id", "fraud_label"]
)

y = df["fraud_label"]


# --------------------------------------------------
# 3. Define feature types
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
# 4. Preprocessing
# --------------------------------------------------

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


# --------------------------------------------------
# 5. Create model
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)


# --------------------------------------------------
# 6. Create complete pipeline
# --------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# --------------------------------------------------
# 7. Train / test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTrain samples:", len(X_train))
print("Test samples:", len(X_test))


# --------------------------------------------------
# 8. Train
# --------------------------------------------------

print("\nTraining Logistic Regression...")

pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# --------------------------------------------------
# 9. Predictions
# --------------------------------------------------

y_pred = pipeline.predict(X_test)

y_probability = pipeline.predict_proba(X_test)[:, 1]


# --------------------------------------------------
# 10. Evaluation
# --------------------------------------------------

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        digits=4
    )
)


print("=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


print("\nROC-AUC:")
print(
    round(
        roc_auc_score(
            y_test,
            y_probability
        ),
        4
    )
)


# --------------------------------------------------
# 11. Save model
# --------------------------------------------------

MODEL_DIR = os.path.join(
    os.path.dirname(__file__),
    "saved_models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "risk_model.pkl"
)

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\nModel saved to:")
print(MODEL_PATH)
