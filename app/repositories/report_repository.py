from app.database import execute, fetch_one


def save_consultation_report(
    consultation_id: int,
    report_title: str,
    summary: str,
    notes: str,
    recommendations: str,
) -> int:
    return execute(
        """
        INSERT INTO consultation_report
            (consultation_id, report_title, summary, notes, recommendations)
        VALUES (%(cid)s, %(title)s, %(summary)s, %(notes)s, %(recs)s)
        RETURNING id
        """,
        {
            "cid": consultation_id,
            "title": report_title,
            "summary": summary,
            "notes": notes,
            "recs": recommendations,
        },
    )


def get_latest_report(consultation_id: int) -> dict | None:
    return fetch_one(
        """
        SELECT id, report_title, summary, notes, recommendations, generated_at
        FROM consultation_report
        WHERE consultation_id = %(cid)s
        ORDER BY generated_at DESC
        LIMIT 1
        """,
        {"cid": consultation_id},
    )
