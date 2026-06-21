"""Train a Random Forest model from consultation history (Phase 6)."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from app.database import fetch_all

MODEL_PATH = Path(__file__).parent / "models" / "disease_model.pkl"


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    rows = fetch_all(
        """
        SELECT
            c.id AS consultation_id,
            c.diagnosis_disease_id AS disease_id,
            cs.symptom_id,
            ce.condition_value_id
        FROM consultation c
        JOIN consultation_symptom cs ON cs.consultation_id = c.id
        LEFT JOIN consultation_environment ce ON ce.consultation_id = c.id
        WHERE c.diagnosis_disease_id IS NOT NULL
        """
    )
    if not rows:
        raise ValueError("No consultation history available for training.")

    df = pd.DataFrame(rows)
    pivot_symptoms = df.pivot_table(
        index="consultation_id",
        columns="symptom_id",
        aggfunc="size",
        fill_value=0,
    )
    pivot_env = df.pivot_table(
        index="consultation_id",
        columns="condition_value_id",
        aggfunc="size",
        fill_value=0,
    )
    features = pivot_symptoms.join(pivot_env, how="outer").fillna(0)
    labels = df.groupby("consultation_id")["disease_id"].first()
    return features, labels


def train_and_save() -> Path:
    x, y = load_training_data()
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)
    score = model.score(x_test, y_test)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_columns": list(x.columns), "accuracy": score}, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH} (test accuracy: {score:.2%})")
    return MODEL_PATH


if __name__ == "__main__":
    train_and_save()
