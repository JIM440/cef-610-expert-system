from app.database import execute, fetch_all, fetch_one


def create_farmer(full_name: str, phone: str, location: str) -> int:
    return execute(
        """
        INSERT INTO farmer (full_name, phone_number, location)
        VALUES (%(full_name)s, %(phone)s, %(location)s)
        RETURNING id
        """,
        {"full_name": full_name, "phone": phone, "location": location},
    )


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
) -> int:
    return execute(
        """
        INSERT INTO consultation (
            performed_by_user_id, farmer_id, crop_id,
            diagnosis_disease_id, confidence_score, consultation_type,
            source, match_tier, gemini_raw_extraction
        )
        VALUES (
            %(performed_by)s, %(farmer_id)s, %(crop_id)s,
            %(disease_id)s, %(confidence)s, %(ctype)s,
            %(source)s, %(match_tier)s, %(gemini_raw)s
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
        },
    )


def add_consultation_symptom(
    consultation_id: int,
    symptom_id: int,
    matched: bool = False,
) -> None:
    execute(
        """
        INSERT INTO consultation_symptom (consultation_id, symptom_id, matched)
        VALUES (%(consultation_id)s, %(symptom_id)s, %(matched)s)
        ON CONFLICT (consultation_id, symptom_id)
        DO UPDATE SET matched = EXCLUDED.matched
        """,
        {
            "consultation_id": consultation_id,
            "symptom_id": symptom_id,
            "matched": matched,
        },
    )


def add_consultation_environment(
    consultation_id: int,
    condition_value_id: int,
    matched: bool = False,
) -> None:
    execute(
        """
        INSERT INTO consultation_environment (
            consultation_id, condition_value_id, matched
        )
        VALUES (%(consultation_id)s, %(condition_value_id)s, %(matched)s)
        ON CONFLICT (consultation_id, condition_value_id)
        DO UPDATE SET matched = EXCLUDED.matched
        """,
        {
            "consultation_id": consultation_id,
            "condition_value_id": condition_value_id,
            "matched": matched,
        },
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
    limit: int = 50,
) -> list[dict]:
    query = """
        SELECT
            c.id AS consultation_id,
            c.consultation_date,
            c.consultation_type,
            c.source,
            c.match_tier,
            c.gemini_raw_extraction,
            c.farmer_id,
            f.full_name AS farmer_name,
            u.username AS performed_by,
            u.full_name AS performed_by_name,
            cr.name AS crop_name,
            d.name AS diagnosed_disease,
            c.confidence_score,
            COALESCE(c.gemini_raw_extraction, ci.visual_summary) AS image_visual_summary,
            COALESCE(c.source, CASE WHEN ci.id IS NULL THEN 'SYMPTOMS' ELSE 'IMAGE' END) AS diagnosis_source,
            ci.analysis_source AS image_analysis_source
        FROM consultation c
        JOIN app_user u ON u.id = c.performed_by_user_id
        LEFT JOIN farmer f ON f.id = c.farmer_id
        JOIN crop cr ON cr.id = c.crop_id
        LEFT JOIN disease d ON d.id = c.diagnosis_disease_id
        LEFT JOIN consultation_image ci ON ci.consultation_id = c.id
        WHERE 1=1
    """
    params: dict = {"limit": limit}
    if farmer_id is not None:
        query += " AND c.farmer_id = %(farmer_id)s"
        params["farmer_id"] = farmer_id
    if performed_by_user_id is not None:
        query += " AND c.performed_by_user_id = %(performed_by)s"
        params["performed_by"] = performed_by_user_id
    if diagnosis_source == "symptom":
        query += " AND c.source = 'SYMPTOMS'"
    elif diagnosis_source == "image":
        query += " AND c.source = 'IMAGE'"
    query += " ORDER BY c.consultation_date DESC LIMIT %(limit)s"
    return fetch_all(query, params)


def get_admin_dashboard_stats() -> dict:
    row = fetch_one(
        """
        SELECT
            (SELECT COUNT(*) FROM farmer) AS farmer_count,
            (SELECT COUNT(*) FROM consultation) AS total_consultations,
            (SELECT COUNT(*) FROM consultation
             WHERE diagnosis_disease_id IS NOT NULL) AS total_diagnoses,
            (SELECT COUNT(*) FROM disease) AS disease_count,
            (SELECT COUNT(*) FROM symptom) AS symptom_count,
            (SELECT COUNT(*) FROM rule) AS rule_count,
            (SELECT COUNT(*) FROM treatment) AS treatment_count,
            (SELECT COUNT(*) FROM crop) AS crop_count,
            (SELECT COUNT(*) FROM consultation
             WHERE diagnosis_disease_id IS NOT NULL
               AND consultation_date >= CURRENT_DATE - INTERVAL '7 days') AS this_week,
            (SELECT COUNT(*) FROM consultation
             WHERE diagnosis_disease_id IS NOT NULL
               AND DATE_TRUNC('month', consultation_date)
                   = DATE_TRUNC('month', CURRENT_DATE)) AS this_month
        """
    )
    if not row:
        return {
            "farmer_count": 0,
            "total_consultations": 0,
            "total_diagnoses": 0,
            "disease_count": 0,
            "symptom_count": 0,
            "rule_count": 0,
            "treatment_count": 0,
            "crop_count": 0,
            "this_week": 0,
            "this_month": 0,
        }
    return dict(row)


def get_farmer_dashboard_stats(farmer_id: int) -> dict:
    total = fetch_one(
        """
        SELECT COUNT(*) AS count FROM consultation
        WHERE farmer_id = %(farmer_id)s AND diagnosis_disease_id IS NOT NULL
        """,
        {"farmer_id": farmer_id},
    )
    this_week = fetch_one(
        """
        SELECT COUNT(*) AS count FROM consultation
        WHERE farmer_id = %(farmer_id)s
          AND diagnosis_disease_id IS NOT NULL
          AND consultation_date >= CURRENT_DATE - INTERVAL '7 days'
        """,
        {"farmer_id": farmer_id},
    )
    this_month = fetch_one(
        """
        SELECT COUNT(*) AS count FROM consultation
        WHERE farmer_id = %(farmer_id)s
          AND diagnosis_disease_id IS NOT NULL
          AND DATE_TRUNC('month', consultation_date) = DATE_TRUNC('month', CURRENT_DATE)
        """,
        {"farmer_id": farmer_id},
    )
    common = fetch_one(
        """
        SELECT d.name AS disease_name, COUNT(*) AS cnt
        FROM consultation c
        JOIN disease d ON d.id = c.diagnosis_disease_id
        WHERE c.farmer_id = %(farmer_id)s
        GROUP BY d.id, d.name
        ORDER BY cnt DESC
        LIMIT 1
        """,
        {"farmer_id": farmer_id},
    )
    return {
        "total": total["count"] if total else 0,
        "this_week": this_week["count"] if this_week else 0,
        "this_month": this_month["count"] if this_month else 0,
        "common_disease": common["disease_name"] if common else "-",
    }


def get_consultation_summary(consultation_id: int) -> dict | None:
    return fetch_one(
        """
        SELECT c.id, c.consultation_date, c.confidence_score, c.consultation_type,
               c.source, c.match_tier, c.gemini_raw_extraction,
               f.full_name AS farmer_name,
               u.username AS performed_by,
               u.full_name AS performed_by_name,
               cr.name AS crop_name,
               d.name AS disease_name,
               dr.explanation, dr.result_title
        FROM consultation c
        JOIN app_user u ON u.id = c.performed_by_user_id
        LEFT JOIN farmer f ON f.id = c.farmer_id
        JOIN crop cr ON cr.id = c.crop_id
        LEFT JOIN disease d ON d.id = c.diagnosis_disease_id
        LEFT JOIN diagnosis_result dr ON dr.consultation_id = c.id
        WHERE c.id = %(id)s
        """,
        {"id": consultation_id},
    )


def get_consultation_image(consultation_id: int) -> dict | None:
    return fetch_one(
        """
        SELECT id, consultation_id, original_filename, analysis_summary,
               visual_summary, analysis_source, gemini_model, created_at
        FROM consultation_image
        WHERE consultation_id = %(id)s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        {"id": consultation_id},
    )
