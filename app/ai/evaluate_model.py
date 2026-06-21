"""Evaluate trained model against held-out consultation data."""

from app.ai.train_model import load_training_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


def evaluate() -> float:
    x, y = load_training_data()
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    scores = cross_val_score(model, x, y, cv=5)
    return float(scores.mean())


if __name__ == "__main__":
    print(f"Cross-validation accuracy: {evaluate():.2%}")
