from app.database import fetch_all


class ReportService:
    def disease_frequency(self) -> list[dict]:
        return fetch_all(
            """
            SELECT d.name AS disease_name, COUNT(c.id) AS consultation_count,
                   ROUND(AVG(c.confidence_score), 1) AS avg_confidence
            FROM consultation c
            JOIN disease d ON d.id = c.diagnosis_disease_id
            WHERE c.diagnosis_disease_id IS NOT NULL
            GROUP BY d.id, d.name
            ORDER BY consultation_count DESC
            """
        )

    def symptom_frequency(self) -> list[dict]:
        return fetch_all(
            """
            SELECT s.name AS symptom_name, COUNT(cs.id) AS occurrence_count
            FROM consultation_symptom cs
            JOIN symptom s ON s.id = cs.symptom_id
            GROUP BY s.id, s.name
            ORDER BY occurrence_count DESC
            """
        )
