from pathlib import Path

import joblib
import pandas as pd

from app.database import execute

MODEL_PATH = Path(__file__).parent / "models" / "disease_model.pkl"


def predict_disease(
    consultation_id: int,
    symptom_ids: list[int],
    condition_value_ids: list[int],
) -> dict | None:
    if not MODEL_PATH.exists():
        return None

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    columns = bundle["feature_columns"]

    row = {col: 0 for col in columns}
    for sid in symptom_ids:
        if sid in row:
            row[sid] = 1
    for cid in condition_value_ids:
        if cid in row:
            row[cid] = 1

    x = pd.DataFrame([row])
    proba = model.predict_proba(x)[0]
    pred_idx = proba.argmax()
    disease_id = int(model.classes_[pred_idx])
    confidence = int(proba[pred_idx] * 100)

    execute(
        """
        INSERT INTO ai_prediction (consultation_id, predicted_disease_id, confidence_score, model_name)
        VALUES (%(cid)s, %(did)s, %(conf)s, %(model)s)
        """,
        {
            "cid": consultation_id,
            "did": disease_id,
            "conf": confidence,
            "model": "RandomForestClassifier",
        },
    )

    return {"disease_id": disease_id, "confidence": confidence}
