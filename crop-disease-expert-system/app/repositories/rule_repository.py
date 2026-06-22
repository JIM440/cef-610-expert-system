from app.database import execute, fetch_all, fetch_one, get_connection
from .crop_repository import TOMATO_CROP_NAME


def get_active_rules_for_crop(crop_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT r.id AS rule_id, r.rule_name, r.confidence_score, r.is_active,
               d.id AS disease_id, d.name AS disease_name, d.explanation_template,
               rs.symptom_id, s.name AS symptom_name, rs.is_required AS symptom_required,
               re.environmental_factor_id, ef.category AS condition_name,
               ef.value_name AS condition_value, re.is_required AS condition_required
        FROM rule r
        JOIN disease d ON d.id = r.disease_id
        LEFT JOIN rule_symptom rs ON rs.rule_id = r.id
        LEFT JOIN symptom s ON s.id = rs.symptom_id
        LEFT JOIN rule_environment re ON re.rule_id = r.id
        LEFT JOIN environmental_factor ef ON ef.id = re.environmental_factor_id
        WHERE d.crop_id = %(crop_id)s AND r.is_active = TRUE
        ORDER BY r.id
        """,
        {"crop_id": crop_id},
    )


def get_all_rules() -> list[dict]:
    return fetch_all(
        """
        SELECT r.id, r.rule_name, r.confidence_score, r.disease_id,
               d.name AS disease_name,
               COALESCE((SELECT string_agg(s.name, ', ' ORDER BY s.name)
                         FROM rule_symptom rs JOIN symptom s ON s.id = rs.symptom_id
                         WHERE rs.rule_id = r.id), '-') AS symptoms,
               COALESCE((SELECT string_agg(ef.category || ': ' || ef.value_name, ', ' ORDER BY ef.category)
                         FROM rule_environment re
                         JOIN environmental_factor ef ON ef.id = re.environmental_factor_id
                         WHERE re.rule_id = r.id), '-') AS conditions,
               COALESCE((SELECT string_agg(t.name, ', ' ORDER BY rt.priority_level, t.name)
                         FROM rule_treatment rt JOIN treatment t ON t.id = rt.treatment_id
                         WHERE rt.rule_id = r.id), '-') AS treatments
        FROM rule r
        JOIN disease d ON d.id = r.disease_id
        JOIN crop c ON c.id = d.crop_id
        WHERE c.name = %(crop)s
        ORDER BY r.rule_name
        """,
        {"crop": TOMATO_CROP_NAME},
    )


def get_rule_detail(rule_id: int) -> dict | None:
    rule = fetch_one(
        """
        SELECT r.id, r.rule_name, r.confidence_score, r.disease_id, d.name AS disease_name
        FROM rule r JOIN disease d ON d.id = r.disease_id
        WHERE r.id = %(id)s
        """,
        {"id": rule_id},
    )
    if not rule:
        return None
    result = dict(rule)
    result["symptom_ids"] = [r["symptom_id"] for r in fetch_all("SELECT symptom_id FROM rule_symptom WHERE rule_id = %(id)s ORDER BY symptom_id", {"id": rule_id})]
    result["condition_value_ids"] = [r["environmental_factor_id"] for r in fetch_all("SELECT environmental_factor_id FROM rule_environment WHERE rule_id = %(id)s ORDER BY environmental_factor_id", {"id": rule_id})]
    result["environmental_factor_ids"] = result["condition_value_ids"]
    result["treatment_ids"] = [r["treatment_id"] for r in fetch_all("SELECT treatment_id FROM rule_treatment WHERE rule_id = %(id)s ORDER BY priority_level, treatment_id", {"id": rule_id})]
    return result


def get_treatments_for_rule(rule_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT t.id, t.name, t.description, rt.priority_level
        FROM rule_treatment rt JOIN treatment t ON t.id = rt.treatment_id
        WHERE rt.rule_id = %(rule_id)s
        ORDER BY rt.priority_level, t.name
        """,
        {"rule_id": rule_id},
    )


def create_rule(disease_id: int, rule_name: str, confidence_score: int, is_active: bool = True) -> int:
    return execute(
        """
        INSERT INTO rule (disease_id, rule_name, confidence_score, is_active)
        VALUES (%(disease_id)s, %(name)s, %(score)s, %(active)s)
        RETURNING id
        """,
        {"disease_id": disease_id, "name": rule_name, "score": confidence_score, "active": is_active},
    )


def update_rule(
    rule_id: int,
    disease_id: int,
    rule_name: str,
    confidence_score: int,
    symptom_ids: list[int],
    environmental_factor_ids: list[int],
    treatment_ids: list[int],
) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE rule SET disease_id=%s, rule_name=%s, confidence_score=%s, is_active=TRUE WHERE id=%s",
                (disease_id, rule_name, confidence_score, rule_id),
            )
            cur.execute("DELETE FROM rule_symptom WHERE rule_id=%s", (rule_id,))
            cur.execute("DELETE FROM rule_environment WHERE rule_id=%s", (rule_id,))
            cur.execute("DELETE FROM rule_treatment WHERE rule_id=%s", (rule_id,))
            for symptom_id in symptom_ids:
                cur.execute("INSERT INTO rule_symptom (rule_id, symptom_id, is_required) VALUES (%s, %s, TRUE)", (rule_id, symptom_id))
            for value_id in environmental_factor_ids:
                cur.execute("INSERT INTO rule_environment (rule_id, environmental_factor_id, is_required) VALUES (%s, %s, TRUE)", (rule_id, value_id))
            for priority, treatment_id in enumerate(treatment_ids, start=1):
                cur.execute("INSERT INTO rule_treatment (rule_id, treatment_id, priority_level) VALUES (%s, %s, %s)", (rule_id, treatment_id, min(priority, 5)))


def link_rule_symptom(rule_id: int, symptom_id: int) -> None:
    execute("INSERT INTO rule_symptom (rule_id, symptom_id, is_required) VALUES (%(rule_id)s, %(symptom_id)s, TRUE) ON CONFLICT (rule_id, symptom_id) DO NOTHING", {"rule_id": rule_id, "symptom_id": symptom_id})


def link_rule_environment(rule_id: int, environmental_factor_id: int) -> None:
    execute("INSERT INTO rule_environment (rule_id, environmental_factor_id, is_required) VALUES (%(rule_id)s, %(value_id)s, TRUE) ON CONFLICT (rule_id, environmental_factor_id) DO NOTHING", {"rule_id": rule_id, "value_id": environmental_factor_id})


def link_rule_treatment(rule_id: int, treatment_id: int, priority: int = 1) -> None:
    execute("INSERT INTO rule_treatment (rule_id, treatment_id, priority_level) VALUES (%(rule_id)s, %(treatment_id)s, %(priority)s) ON CONFLICT (rule_id, treatment_id) DO UPDATE SET priority_level=EXCLUDED.priority_level", {"rule_id": rule_id, "treatment_id": treatment_id, "priority": priority})