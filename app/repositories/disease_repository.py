"""
Disease Knowledge repository — FACTS only.

Answers: "What is true about this disease?"

Manages: disease, disease_symptom, disease_environment, disease_treatment

Used by: Diseases page, disease details, knowledge base, reports, AI training data.

Does NOT perform diagnosis. For reasoning, use RuleRepository + InferenceEngine.
"""

from app.database import execute, fetch_all, fetch_one
from .crop_repository import TOMATO_CROP_NAME


def get_diseases_by_crop(crop_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT id, name, description, explanation_template, crop_id
        FROM disease
        WHERE crop_id = %(crop_id)s
        ORDER BY name
        """,
        {"crop_id": crop_id},
    )


def get_all_diseases() -> list[dict]:
    return fetch_all(
        """
        SELECT d.id, d.name, d.description, d.explanation_template
        FROM disease d
        JOIN crop c ON c.id = d.crop_id
        WHERE c.name = %(crop)s
        ORDER BY d.name
        """,
        {"crop": TOMATO_CROP_NAME},
    )


def get_disease_by_id(disease_id: int) -> dict | None:
    return fetch_one(
        """
        SELECT id, crop_id, name, description, explanation_template
        FROM disease WHERE id = %(id)s
        """,
        {"id": disease_id},
    )


def create_disease(
    crop_id: int, name: str, description: str, explanation_template: str
) -> int:
    return execute(
        """
        INSERT INTO disease (crop_id, name, description, explanation_template)
        VALUES (%(crop_id)s, %(name)s, %(desc)s, %(template)s)
        RETURNING id
        """,
        {
            "crop_id": crop_id,
            "name": name,
            "desc": description,
            "template": explanation_template,
        },
    )


def update_disease(
    disease_id: int, name: str, description: str, explanation_template: str
) -> None:
    execute(
        """
        UPDATE disease
        SET name = %(name)s, description = %(desc)s,
            explanation_template = %(template)s
        WHERE id = %(id)s
        """,
        {
            "id": disease_id,
            "name": name,
            "desc": description,
            "template": explanation_template,
        },
    )


def get_symptoms_for_disease(disease_id: int) -> list[dict]:
    """Factual symptom associations — not diagnosis requirements."""
    return fetch_all(
        """
        SELECT s.id, s.name, s.description, ds.weight
        FROM disease_symptom ds
        JOIN symptom s ON s.id = ds.symptom_id
        WHERE ds.disease_id = %(disease_id)s
        ORDER BY ds.weight DESC, s.name
        """,
        {"disease_id": disease_id},
    )


def link_disease_symptom(disease_id: int, symptom_id: int, weight: int = 1) -> None:
    execute(
        """
        INSERT INTO disease_symptom (disease_id, symptom_id, weight)
        VALUES (%(disease_id)s, %(symptom_id)s, %(weight)s)
        ON CONFLICT (disease_id, symptom_id) DO UPDATE SET weight = EXCLUDED.weight
        """,
        {"disease_id": disease_id, "symptom_id": symptom_id, "weight": weight},
    )


def unlink_disease_symptom(disease_id: int, symptom_id: int) -> None:
    execute(
        """
        DELETE FROM disease_symptom
        WHERE disease_id = %(disease_id)s AND symptom_id = %(symptom_id)s
        """,
        {"disease_id": disease_id, "symptom_id": symptom_id},
    )


def get_environments_for_disease(disease_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT ec.name AS condition_name, ecv.value_name, de.weight
        FROM disease_environment de
        JOIN environmental_condition_value ecv ON ecv.id = de.condition_value_id
        JOIN environmental_condition ec ON ec.id = ecv.condition_id
        WHERE de.disease_id = %(disease_id)s
        ORDER BY ec.name, ecv.value_name
        """,
        {"disease_id": disease_id},
    )


def get_treatments_for_disease(disease_id: int) -> list[dict]:
    """General treatments associated with a disease (factual knowledge)."""
    return fetch_all(
        """
        SELECT t.id, t.name, t.description, dt.priority_level
        FROM disease_treatment dt
        JOIN treatment t ON t.id = dt.treatment_id
        WHERE dt.disease_id = %(disease_id)s
        ORDER BY dt.priority_level, t.name
        """,
        {"disease_id": disease_id},
    )


def link_disease_treatment(
    disease_id: int, treatment_id: int, priority_level: int = 1
) -> None:
    execute(
        """
        INSERT INTO disease_treatment (disease_id, treatment_id, priority_level)
        VALUES (%(disease_id)s, %(treatment_id)s, %(priority)s)
        ON CONFLICT (disease_id, treatment_id) DO UPDATE
        SET priority_level = EXCLUDED.priority_level
        """,
        {
            "disease_id": disease_id,
            "treatment_id": treatment_id,
            "priority": priority_level,
        },
    )


def get_disease_knowledge_summary(disease_id: int) -> dict | None:
    """Full factual profile for disease detail views."""
    disease = get_disease_by_id(disease_id)
    if not disease:
        return None
    return {
        "disease": disease,
        "symptoms": get_symptoms_for_disease(disease_id),
        "environments": get_environments_for_disease(disease_id),
        "treatments": get_treatments_for_disease(disease_id),
    }


def delete_disease(disease_id: int) -> None:
    execute("DELETE FROM disease WHERE id = %(id)s", {"id": disease_id})
