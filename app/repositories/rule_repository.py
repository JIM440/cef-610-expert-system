from app.database import execute, fetch_all
from .crop_repository import TOMATO_CROP_NAME


def get_active_rules_for_crop(crop_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT
            r.id AS rule_id,
            r.rule_name,
            r.confidence_score,
            r.is_active,
            d.id AS disease_id,
            d.name AS disease_name,
            d.explanation_template,
            rs.symptom_id,
            s.name AS symptom_name,
            rs.is_required AS symptom_required,
            re.condition_value_id,
            ec.name AS condition_name,
            ecv.value_name AS condition_value,
            re.is_required AS condition_required
        FROM rule r
        JOIN disease d ON d.id = r.disease_id
        LEFT JOIN rule_symptom rs ON rs.rule_id = r.id
        LEFT JOIN symptom s ON s.id = rs.symptom_id
        LEFT JOIN rule_environment re ON re.rule_id = r.id
        LEFT JOIN environmental_condition_value ecv ON ecv.id = re.condition_value_id
        LEFT JOIN environmental_condition ec ON ec.id = ecv.condition_id
        WHERE d.crop_id = %(crop_id)s AND r.is_active = TRUE
        ORDER BY r.id
        """,
        {"crop_id": crop_id},
    )


def get_all_rules() -> list[dict]:
    return fetch_all(
        """
        SELECT r.id, r.rule_name, r.confidence_score, r.is_active,
               CASE WHEN r.is_active THEN 'Active' ELSE 'Inactive' END AS active_status,
               d.name AS disease_name
        FROM rule r
        JOIN disease d ON d.id = r.disease_id
        JOIN crop c ON c.id = d.crop_id
        WHERE c.name = %(crop)s
        ORDER BY r.id
        """,
        {"crop": TOMATO_CROP_NAME},
    )


def get_treatments_for_rule(rule_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT t.id, t.name, t.description, rt.priority_level
        FROM rule_treatment rt
        JOIN treatment t ON t.id = rt.treatment_id
        WHERE rt.rule_id = %(rule_id)s
        ORDER BY rt.priority_level, t.name
        """,
        {"rule_id": rule_id},
    )


def create_rule(
    disease_id: int, rule_name: str, confidence_score: int, is_active: bool = True
) -> int:
    return execute(
        """
        INSERT INTO rule (disease_id, rule_name, confidence_score, is_active)
        VALUES (%(disease_id)s, %(name)s, %(score)s, %(active)s)
        RETURNING id
        """,
        {
            "disease_id": disease_id,
            "name": rule_name,
            "score": confidence_score,
            "active": is_active,
        },
    )


def update_rule_active(rule_id: int, is_active: bool) -> None:
    execute(
        "UPDATE rule SET is_active = %(active)s WHERE id = %(id)s",
        {"id": rule_id, "active": is_active},
    )


def link_rule_symptom(rule_id: int, symptom_id: int) -> None:
    execute(
        """
        INSERT INTO rule_symptom (rule_id, symptom_id, is_required)
        VALUES (%(rule_id)s, %(symptom_id)s, TRUE)
        ON CONFLICT (rule_id, symptom_id) DO NOTHING
        """,
        {"rule_id": rule_id, "symptom_id": symptom_id},
    )


def link_rule_environment(rule_id: int, condition_value_id: int) -> None:
    execute(
        """
        INSERT INTO rule_environment (rule_id, condition_value_id, is_required)
        VALUES (%(rule_id)s, %(value_id)s, TRUE)
        ON CONFLICT (rule_id, condition_value_id) DO NOTHING
        """,
        {"rule_id": rule_id, "value_id": condition_value_id},
    )


def link_rule_treatment(rule_id: int, treatment_id: int, priority: int = 1) -> None:
    execute(
        """
        INSERT INTO rule_treatment (rule_id, treatment_id, priority_level)
        VALUES (%(rule_id)s, %(treatment_id)s, %(priority)s)
        ON CONFLICT (rule_id, treatment_id) DO NOTHING
        """,
        {"rule_id": rule_id, "treatment_id": treatment_id, "priority": priority},
    )
