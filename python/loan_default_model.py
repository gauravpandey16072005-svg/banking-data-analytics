"""Baseline loan-default classifier for the synthetic banking dataset.

Run from the repository root:
    python -m pip install -r requirements.txt
    python python/loan_default_model.py

Important: loan_status was randomly assigned by the synthetic-data generator.
Metrics are a pipeline demonstration, not evidence of real-world predictive power.
"""
from pathlib import Path
import json

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "loans.csv"
CUSTOMERS_PATH = ROOT / "data" / "raw" / "customers.csv"
OUTPUT_DIR = ROOT / "outputs"
TARGET = "is_default"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Loan data not found: {DATA_PATH}")

    loans = pd.read_csv(DATA_PATH)
    required = {
        "loan_status", "loan_amount", "interest_rate",
        "loan_term_months", "monthly_payment", "loan_type",
    }
    missing = sorted(required - set(loans.columns))
    if missing:
        raise ValueError(f"loans.csv is missing required columns: {missing}")

    # Optional customer age feature; safely skip it if the customer file/schema differs.
    if CUSTOMERS_PATH.exists() and "customer_id" in loans.columns:
        customers = pd.read_csv(CUSTOMERS_PATH)
        if {"customer_id", "age"}.issubset(customers.columns):
            loans = loans.merge(
                customers[["customer_id", "age"]].drop_duplicates("customer_id"),
                on="customer_id", how="left", validate="many_to_one",
            )

    loans["loan_status"] = loans["loan_status"].astype(str).str.strip().str.title()
    loans = loans[loans["loan_status"].isin(["Active", "Closed", "Defaulted"])].copy()
    loans[TARGET] = (loans["loan_status"] == "Defaulted").astype(int)

    numeric_features = [
        c for c in ["loan_amount", "interest_rate", "loan_term_months",
                    "monthly_payment", "age"] if c in loans.columns
    ]
    categorical_features = ["loan_type"]
    features = numeric_features + categorical_features
    data = loans[features + [TARGET]].copy()
    data = data.replace([float("inf"), float("-inf")], float("nan")).dropna(subset=[TARGET])

    if data[TARGET].nunique() != 2 or data[TARGET].value_counts().min() < 2:
        raise ValueError("Need at least two examples from each target class to train.")

    X, y = data[features], data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    numeric_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    categorical_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])
    preprocess = ColumnTransformer([
        ("numeric", numeric_pipe, numeric_features),
        ("categorical", categorical_pipe, categorical_features),
    ])
    model = Pipeline([
        ("preprocess", preprocess),
        ("classifier", LogisticRegression(
            max_iter=2000, class_weight="balanced", random_state=42
        )),
    ])
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    metrics = {
        "rows_used": int(len(data)),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "default_rate": round(float(y.mean()), 4),
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision_default": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall_default": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1_default": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "confusion_matrix_labels_[0,1]": confusion_matrix(y_test, predictions, labels=[0, 1]).tolist(),
        "features": features,
        "target_definition": "1 = loan_status Defaulted; 0 = Active or Closed",
        "caveat": "Synthetic loan statuses were randomly generated; metrics are for demonstration only.",
    }

    OUTPUT_DIR.mkdir(exist_ok=True)
    joblib.dump(model, OUTPUT_DIR / "loan_default_logistic_regression.joblib")
    (OUTPUT_DIR / "loan_default_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    pd.DataFrame({
        "actual_default": y_test.to_numpy(),
        "predicted_default": predictions,
        "predicted_default_probability": probabilities,
    }).to_csv(OUTPUT_DIR / "loan_default_test_predictions.csv", index=False)

    print("\nLOAN DEFAULT BASELINE — HELD-OUT TEST SET")
    print(json.dumps(metrics, indent=2))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, target_names=["Not defaulted", "Defaulted"], zero_division=0))
    print(f"\nSaved model and evaluation files to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
