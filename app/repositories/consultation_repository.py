from app.database import execute, fetch_all, fetch_one


def create_consultation(
    performed_by_user_id: int,
    consultation_type: str,
    crop_id: int,
    disease_id: int | None,
    confidence: int | None,
    farmer_id: int | None = None,
    source: str = "SYMPTOMS",
    match_tier: str = "HIGH",
    gemini_raw_extraction: str | None = None,
    matched_rule_id: int | None = None,
    explanation: str | None = None,
    ai_predicted_disease_id: int | None = None,
    ai_confidence: int | None = None,
    ai_model_version: str | None = None,
) -> int:
    return execute(
        """
        INSERT INTO consultation (
            performed_by_user_id, farmer_id, crop_id,
            final_disease_id, final_confidence, consultation_type,
            source, match_tier, gemini_raw_extraction,
            matched_rule_id, explanation,
            ai_predicted_disease_id, ai_confidence, ai_model_version
        )
        VALUES (
            %(performed_by)s, %(farmer_id)s, %(crop_id)s,
            %(disease_id)s, %(confidence)s, %(ctype)s,
            %(source)s, %(match_tier)s, %(gemini_raw)s,
            %(matched_rule_id)s, %(explanation)s,
            %(ai_disease_id)s, %(ai_confidence)s, %(ai_model_version)s
        )
        RETURNING id
        """,
        {
            "performed_by": performed_by_user_id,
            "farmer_id": farmer_id,
            "crop_id": crop_id,
            "disease_id": disease_id,
            "confidence": confidence,
            "ctype": consultation_type,
            "source": source,
            "match_tier": match_tier,
            "gemini_raw": gemini_raw_extraction,
            "matched_rule_id": matched_rule_id,
            "explanation": explanation,
            "ai_disease_id": ai_predicted_disease_id,
            "ai_confidence": ai_confidence,
            "ai_model_version": ai_model_version,
        },
    )


def add_consultation_symptom(consultation_id: int, symptom_id: int, matched: bool = False) -> None:
    execute(
        """
        INSERT INTO consultation_symptom (consultation_id, symptom_id, matched)
        VALUES (%(consultation_id)s, %(symptom_id)s, %(matched)s)
        ON CONFLICT (consultation_id, symptom_id)
        DO UPDATE SET matched=EXCLUDED.matched
        """,
        {"consultation_id": consultation_id, "symptom_id": symptom_id, "matched": matched},
    )


def add_consultation_environment(
    consultation_id: int, environmental_factor_id: int, matched: bool = False
) -> None:
    execute(
        """
        INSERT INTO consultation_environment (
            consultation_id, environmental_factor_id, matched
        ) VALUES (%(consultation_id)s, %(factor_id)s, %(matched)s)
        ON CONFLICT (consultation_id, environmental_factor_id)
        DO UPDATE SET matched=EXCLUDED.matched
        """,
        {"consultation_id": consultation_id, "factor_id": environmental_factor_id, "matched": matched},
    )


def add_consultation_treatment(consultation_id: int, treatment_id: int) -> None:
    execute(
        """
        INSERT INTO consultation_treatment (consultation_id, treatment_id)
        VALUES (%(consultation_id)s, %(treatment_id)s)
        ON CONFLICT (consultation_id, treatment_id) DO NOTHING
        """,
        {"consultation_id": consultation_id, "treatment_id": treatment_id},
    )


def get_consultation_history(
    farmer_id: int | None = None,
    performed_by_user_id: int | None = None,
    diagnosis_source: str = "all",
    limit: int | None = None,
) -> list[dict]:
    query = """
        SELECT c.id AS consultation_id, c.consultation_date,
               c.consultation_type, c.source, c.match_tier,
               c.gemini_raw_extraction, c.farmer_id, c.explanation,
               f.full_name AS farmer_name,
               u.username AS performed_by, u.full_name AS performed_by_name,
               cr.name AS crop_name, d.name AS diagnosed_disease,
               c.final_confidence AS confidence_score,
               ai_d.name AS ai_predicted_disease,
               c.ai_predicted_disease_id, c.ai_confidence, c.ai_model_version,
               CASE
                   WHEN c.final_disease_id IS NULL OR c.ai_predicted_disease_id IS NULL THEN NULL
                   ELSE c.final_disease_id=c.ai_predicted_disease_id
               END AS methods_agree,
               COALESCE((
                   SELECT string_agg(s.name, ', ' ORDER BY s.name)
                   FROM consultation_symptom cs
                   JOIN symptom s ON s.id=cs.symptom_id
                   WHERE cs.consultation_id=c.id
               ), '-') AS symptoms,
               COALESCE((
                   SELECT string_agg(t.name, ', ' ORDER BY ct.id)
                   FROM consultation_treatment ct
                   JOIN treatment t ON t.id=ct.treatment_id
                   WHERE ct.consultation_id=c.id
               ), '-') AS treatments,
               c.gemini_raw_extraction AS image_visual_summary,
               c.source AS diagnosis_source,
               CASE WHEN c.source='IMAGE' THEN 'gemini' END AS image_analysis_source
        FROM consultation c
        JOIN app_user u ON u.id=c.performed_by_user_id
        LEFT JOIN app_user f ON f.id=c.farmer_id AND f.role='FARMER'
        JOIN crop cr ON cr.id=c.crop_id
        LEFT JOIN disease d ON d.id=c.final_disease_id
        LEFT JOIN disease ai_d ON ai_d.id=c.ai_predicted_disease_id
        WHERE 1=1
    """
    params: dict = {}
    if farmer_id is not None:
        query += " AND c.farmer_id=%(farmer_id)s"
        params["farmer_id"] = farmer_id
    if performed_by_user_id is not None:
        query += " AND c.performed_by_user_id=%(performed_by)s"
        params["performed_by"] = performed_by_user_id
    if diagnosis_source == "symptom":
        query += " AND c.source='SYMPTOMS'"
    elif diagnosis_source == "image":
        query += " AND c.source='IMAGE'"
    query += " ORDER BY c.consultation_date DESC"
    if limit is not None:
        query += " LIMIT %(limit)s"
        params["limit"] = limit
    return fetch_all(query, params)


def get_admin_dashboard_stats() -> dict:
    return dict(fetch_one(
        """
        SELECT
          (SELECT COUNT(*) FROM app_user WHERE role='FARMER') AS farmer_count,
          (SELECT COUNT(*) FROM consultation) AS total_consultations,
          (SELECT COUNT(*) FROM consultation WHERE final_disease_id IS NOT NULL) AS total_diagnoses,
          (SELECT COUNT(*) FROM disease) AS disease_count,
          (SELECT COUNT(*) FROM symptom) AS symptom_count,
          (SELECT COUNT(*) FROM rule) AS rule_count,
          (SELECT COUNT(*) FROM treatment) AS treatment_count,
          (SELECT COUNT(*) FROM crop) AS crop_count,
          (SELECT COUNT(*) FROM consultation WHERE final_disease_id IS NOT NULL
             AND consultation_date >= CURRENT_DATE - INTERVAL '7 days') AS this_week,
          (SELECT COUNT(*) FROM consultation WHERE final_disease_id IS NOT NULL
             AND DATE_TRUNC('month', consultation_date)=DATE_TRUNC('month', CURRENT_DATE)) AS this_month
        """
    ))


def get_farmer_dashboard_stats(farmer_id: int) -> dict:
    row = fetch_one(
        """
        SELECT
          COUNT(*) FILTER (WHERE final_disease_id IS NOT NULL) AS total,
          COUNT(*) FILTER (WHERE final_disease_id IS NOT NULL AND consultation_date >= CURRENT_DATE-INTERVAL '7 days') AS this_week,
          COUNT(*) FILTER (WHERE final_disease_id IS NOT NULL AND DATE_TRUNC('month',consultation_date)=DATE_TRUNC('month',CURRENT_DATE)) AS this_month
        FROM consultation WHERE farmer_id=%(farmer_id)s
        """,
        {"farmer_id": farmer_id},
    )
    common = fetch_one(
        """
        SELECT d.name AS disease_name, COUNT(*) AS cnt
        FROM consultation c JOIN disease d ON d.id=c.final_disease_id
        WHERE c.farmer_id=%(farmer_id)s
        GROUP BY d.id,d.name ORDER BY cnt DESC LIMIT 1
        """,
        {"farmer_id": farmer_id},
    )
    return {"total": row["total"], "this_week": row["this_week"],
            "this_month": row["this_month"],
            "common_disease": common["disease_name"] if common else "-"}
