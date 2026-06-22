"""Knowledge-base-derived Naive Bayes disease predictor.

This component applies actual Naive Bayes probability math at runtime. It is
not fitted from a held-out historical dataset: priors and likelihoods are
rebuilt from disease_symptom, rule_symptom, and rule_environment evidence.
"""

from dataclasses import dataclass
from math import exp, log

from app.database import fetch_all


@dataclass(frozen=True)
class AIPrediction:
    disease_id: int
    disease_name: str
    confidence: int
    model_version: str
    probabilities: dict[int, float]


class NaiveBayesPredictor:
    model_version = "naive_bayes_v1"

    def __init__(self, alpha: float = 1.0) -> None:
        if alpha <= 0:
            raise ValueError("Laplace smoothing alpha must be positive.")
        self.alpha = alpha

    def predict(
        self,
        symptom_ids: list[int],
        environmental_factor_ids: list[int] | None = None,
        crop_id: int | None = None,
    ) -> AIPrediction | None:
        selected_symptoms = sorted(set(symptom_ids))
        if not selected_symptoms:
            return None

        selected_factors = sorted(set(environmental_factor_ids or []))
        diseases = self._load_diseases(crop_id)
        if not diseases:
            return None

        symptom_rows = self._load_symptom_evidence(crop_id)
        environment_rows = self._load_environment_evidence(crop_id)
        symptom_vocabulary = max(self._symptom_vocabulary_size(), 1)
        environment_vocabulary = max(self._environment_vocabulary_size(), 1)

        symptom_evidence: dict[int, dict[int, float]] = {d["id"]: {} for d in diseases}
        symptom_totals: dict[int, float] = {d["id"]: 0.0 for d in diseases}
        for row in symptom_rows:
            disease_id = row["disease_id"]
            symptom_id = row["symptom_id"]
            weight = float(row["evidence_weight"] or 0)
            symptom_evidence.setdefault(disease_id, {})[symptom_id] = weight
            symptom_totals[disease_id] = symptom_totals.get(disease_id, 0.0) + weight

        environment_evidence: dict[int, dict[int, float]] = {d["id"]: {} for d in diseases}
        environment_totals: dict[int, float] = {d["id"]: 0.0 for d in diseases}
        for row in environment_rows:
            disease_id = row["disease_id"]
            factor_id = row["environmental_factor_id"]
            weight = float(row["evidence_weight"] or 0)
            environment_evidence.setdefault(disease_id, {})[factor_id] = weight
            environment_totals[disease_id] = environment_totals.get(disease_id, 0.0) + weight

        evidence_mass = {
            disease["id"]: symptom_totals.get(disease["id"], 0.0)
            + environment_totals.get(disease["id"], 0.0)
            for disease in diseases
        }
        total_mass = sum(evidence_mass.values())
        disease_count = len(diseases)

        log_scores: dict[int, float] = {}
        for disease in diseases:
            disease_id = disease["id"]
            prior = (evidence_mass[disease_id] + self.alpha) / (
                total_mass + self.alpha * disease_count
            )
            score = log(prior)

            symptom_denominator = symptom_totals[disease_id] + self.alpha * symptom_vocabulary
            for symptom_id in selected_symptoms:
                numerator = symptom_evidence[disease_id].get(symptom_id, 0.0) + self.alpha
                score += log(numerator / symptom_denominator)

            if selected_factors:
                environment_denominator = (
                    environment_totals[disease_id] + self.alpha * environment_vocabulary
                )
                for factor_id in selected_factors:
                    numerator = environment_evidence[disease_id].get(factor_id, 0.0) + self.alpha
                    score += log(numerator / environment_denominator)

            log_scores[disease_id] = score

        max_log = max(log_scores.values())
        unnormalized = {
            disease_id: exp(score - max_log) for disease_id, score in log_scores.items()
        }
        normalizer = sum(unnormalized.values())
        probabilities = {
            disease_id: value / normalizer for disease_id, value in unnormalized.items()
        }
        best_id = max(probabilities, key=probabilities.get)
        name_by_id = {d["id"]: d["name"] for d in diseases}
        return AIPrediction(
            disease_id=best_id,
            disease_name=name_by_id[best_id],
            confidence=round(probabilities[best_id] * 100),
            model_version=self.model_version,
            probabilities=probabilities,
        )

    @staticmethod
    def _load_diseases(crop_id: int | None) -> list[dict]:
        query = "SELECT id, name FROM disease"
        params: dict = {}
        if crop_id is not None:
            query += " WHERE crop_id=%(crop_id)s"
            params["crop_id"] = crop_id
        query += " ORDER BY id"
        return fetch_all(query, params)

    @staticmethod
    def _load_symptom_evidence(crop_id: int | None) -> list[dict]:
        query = """
            SELECT d.id AS disease_id, s.id AS symptom_id,
                   COALESCE(ds.weight, 0) + COALESCE(rs.rule_count, 0) AS evidence_weight
            FROM disease d
            CROSS JOIN symptom s
            LEFT JOIN disease_symptom ds
              ON ds.disease_id=d.id AND ds.symptom_id=s.id
            LEFT JOIN (
                SELECT r.disease_id, rs.symptom_id, COUNT(*)::INTEGER AS rule_count
                FROM rule_symptom rs
                JOIN rule r ON r.id=rs.rule_id
                WHERE r.is_active=TRUE
                GROUP BY r.disease_id, rs.symptom_id
            ) rs ON rs.disease_id=d.id AND rs.symptom_id=s.id
            WHERE (ds.weight IS NOT NULL OR rs.rule_count IS NOT NULL)
        """
        params: dict = {}
        if crop_id is not None:
            query += " AND d.crop_id=%(crop_id)s"
            params["crop_id"] = crop_id
        return fetch_all(query, params)

    @staticmethod
    def _load_environment_evidence(crop_id: int | None) -> list[dict]:
        query = """
            SELECT r.disease_id, re.environmental_factor_id,
                   COUNT(*)::INTEGER AS evidence_weight
            FROM rule_environment re
            JOIN rule r ON r.id=re.rule_id
            JOIN disease d ON d.id=r.disease_id
            WHERE r.is_active=TRUE
        """
        params: dict = {}
        if crop_id is not None:
            query += " AND d.crop_id=%(crop_id)s"
            params["crop_id"] = crop_id
        query += " GROUP BY r.disease_id, re.environmental_factor_id"
        return fetch_all(query, params)

    @staticmethod
    def _symptom_vocabulary_size() -> int:
        rows = fetch_all("SELECT COUNT(*) AS count FROM symptom")
        return int(rows[0]["count"]) if rows else 0

    @staticmethod
    def _environment_vocabulary_size() -> int:
        rows = fetch_all("SELECT COUNT(*) AS count FROM environmental_factor")
        return int(rows[0]["count"]) if rows else 0
