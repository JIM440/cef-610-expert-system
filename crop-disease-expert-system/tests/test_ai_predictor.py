import pytest

from app.expert_system.ai_predictor import NaiveBayesPredictor


def _predictor(
    monkeypatch,
    symptom_rows,
    environment_rows=None,
    symptom_vocabulary=3,
    environment_vocabulary=2,
):
    predictor = NaiveBayesPredictor(alpha=1.0)
    monkeypatch.setattr(
        predictor,
        "_load_diseases",
        lambda crop_id: [
            {"id": 1, "name": "Disease A"},
            {"id": 2, "name": "Disease B"},
        ],
    )
    monkeypatch.setattr(predictor, "_load_symptom_evidence", lambda crop_id: symptom_rows)
    monkeypatch.setattr(
        predictor,
        "_load_environment_evidence",
        lambda crop_id: environment_rows or [],
    )
    monkeypatch.setattr(predictor, "_symptom_vocabulary_size", lambda: symptom_vocabulary)
    monkeypatch.setattr(
        predictor,
        "_environment_vocabulary_size",
        lambda: environment_vocabulary,
    )
    return predictor


def test_weighted_symptom_evidence_selects_expected_disease(monkeypatch):
    predictor = _predictor(
        monkeypatch,
        [
            {"disease_id": 1, "symptom_id": 10, "evidence_weight": 6},
            {"disease_id": 2, "symptom_id": 20, "evidence_weight": 6},
        ],
    )

    result = predictor.predict([10], [], crop_id=1)

    assert result is not None
    assert result.disease_id == 1
    assert result.model_version == "naive_bayes_v1"
    assert result.confidence > 50
    assert sum(result.probabilities.values()) == pytest.approx(1.0)


def test_environmental_evidence_contributes_to_prediction(monkeypatch):
    predictor = _predictor(
        monkeypatch,
        [
            {"disease_id": 1, "symptom_id": 10, "evidence_weight": 2},
            {"disease_id": 2, "symptom_id": 10, "evidence_weight": 2},
        ],
        [
            {"disease_id": 1, "environmental_factor_id": 5, "evidence_weight": 5},
            {"disease_id": 2, "environmental_factor_id": 6, "evidence_weight": 5},
        ],
    )

    result = predictor.predict([10], [5], crop_id=1)

    assert result is not None
    assert result.disease_id == 1


def test_prediction_requires_at_least_one_symptom(monkeypatch):
    predictor = _predictor(monkeypatch, [])
    assert predictor.predict([], [5], crop_id=1) is None
