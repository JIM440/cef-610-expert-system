from app.database import execute, fetch_all, fetch_one


def get_reason_type_id(code: str) -> int | None:
    row = fetch_one(
        "SELECT id FROM reason_type WHERE code = %(code)s",
        {"code": code},
    )
    return row["id"] if row else None


def save_diagnosis_result(
    consultation_id: int,
    disease_id: int,
    result_title: str,
    explanation: str,
    confidence: int,
) -> int:
    return execute(
        """
        INSERT INTO diagnosis_result
            (consultation_id, disease_id, result_title, explanation, confidence_score)
        VALUES
            (%(consultation_id)s, %(disease_id)s, %(title)s, %(explanation)s, %(confidence)s)
        RETURNING id
        """,
        {
            "consultation_id": consultation_id,
            "disease_id": disease_id,
            "title": result_title,
            "explanation": explanation,
            "confidence": confidence,
        },
    )


def save_diagnosis_reason(
    diagnosis_result_id: int,
    reason_type_id: int,
    related_rule_id: int | None,
    display_order: int,
) -> int:
    return execute(
        """
        INSERT INTO diagnosis_reason
            (diagnosis_result_id, reason_type_id, related_rule_id, display_order)
        VALUES (%(result_id)s, %(type_id)s, %(rule_id)s, %(order)s)
        RETURNING id
        """,
        {
            "result_id": diagnosis_result_id,
            "type_id": reason_type_id,
            "rule_id": related_rule_id,
            "order": display_order,
        },
    )


def link_reason_symptom(diagnosis_reason_id: int, symptom_id: int) -> None:
    execute(
        """
        INSERT INTO diagnosis_reason_symptom (diagnosis_reason_id, symptom_id)
        VALUES (%(reason_id)s, %(symptom_id)s)
        ON CONFLICT (diagnosis_reason_id, symptom_id) DO NOTHING
        """,
        {"reason_id": diagnosis_reason_id, "symptom_id": symptom_id},
    )


def link_reason_environment(diagnosis_reason_id: int, condition_value_id: int) -> None:
    execute(
        """
        INSERT INTO diagnosis_reason_environment (diagnosis_reason_id, condition_value_id)
        VALUES (%(reason_id)s, %(value_id)s)
        ON CONFLICT (diagnosis_reason_id, condition_value_id) DO NOTHING
        """,
        {"reason_id": diagnosis_reason_id, "value_id": condition_value_id},
    )


def save_rule_match(diagnosis_result_id: int, rule_id: int, matched_score: int) -> None:
    execute(
        """
        INSERT INTO diagnosis_rule_match (diagnosis_result_id, rule_id, matched_score)
        VALUES (%(result_id)s, %(rule_id)s, %(score)s)
        ON CONFLICT (diagnosis_result_id, rule_id) DO NOTHING
        """,
        {"result_id": diagnosis_result_id, "rule_id": rule_id, "score": matched_score},
    )


def get_diagnosis_detail(consultation_id: int) -> list[dict]:
    return fetch_all(
        """
        SELECT
            dr.id AS diagnosis_result_id,
            dr.result_title,
            dr.explanation,
            dr.confidence_score,
            c.consultation_type,
            dis.name AS disease_name,
            dre.id AS reason_id,
            rt.code AS reason_type_code,
            rt.label AS reason_type_label,
            drm.rule_id,
            ru.rule_name,
            drm.matched_score,
            drs.symptom_id,
            sym.name AS reason_symptom_name,
            dre_env.condition_value_id,
            ec.name AS reason_condition_name,
            ecv.value_name AS reason_condition_value
        FROM diagnosis_result dr
        JOIN consultation c ON c.id = dr.consultation_id
        JOIN disease dis ON dis.id = dr.disease_id
        LEFT JOIN diagnosis_reason dre ON dre.diagnosis_result_id = dr.id
        LEFT JOIN reason_type rt ON rt.id = dre.reason_type_id
        LEFT JOIN diagnosis_rule_match drm ON drm.diagnosis_result_id = dr.id
        LEFT JOIN rule ru ON ru.id = drm.rule_id
        LEFT JOIN diagnosis_reason_symptom drs ON drs.diagnosis_reason_id = dre.id
        LEFT JOIN symptom sym ON sym.id = drs.symptom_id
        LEFT JOIN diagnosis_reason_environment dre_env ON dre_env.diagnosis_reason_id = dre.id
        LEFT JOIN environmental_condition_value ecv ON ecv.id = dre_env.condition_value_id
        LEFT JOIN environmental_condition ec ON ec.id = ecv.condition_id
        WHERE dr.consultation_id = %(consultation_id)s
        ORDER BY dre.display_order
        """,
        {"consultation_id": consultation_id},
    )
