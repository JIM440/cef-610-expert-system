from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extras

from app.config import DB_CONFIG

REQUIRED_SCHEMA_COLUMNS = {
    "app_user": {"role", "phone_number", "location", "email", "updated_at"},
    "consultation": {"source", "gemini_raw_extraction", "match_tier", "final_disease_id", "final_confidence", "matched_rule_id", "explanation"},
    "consultation_symptom": {"matched"},
    "consultation_environment": {"environmental_factor_id", "matched"},
    "rule_environment": {"environmental_factor_id"},
    "environmental_factor": {"category", "value_name", "unit"},
}


def test_connection() -> tuple[bool, str]:
    try:
        with psycopg2.connect(DB_CONFIG.dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return True, ""
    except Exception as exc:
        return False, str(exc)


def get_schema_issues() -> list[str]:
    expected = {
        (table_name, column_name)
        for table_name, columns in REQUIRED_SCHEMA_COLUMNS.items()
        for column_name in columns
    }
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name, column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = ANY(%s)
                """,
                (list(REQUIRED_SCHEMA_COLUMNS),),
            )
            existing = set(cur.fetchall())

    issues = [
        f"{table_name}.{column_name}"
        for table_name, column_name in sorted(expected - existing)
    ]
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                """
            )
            table_count = cur.fetchone()[0]
            if table_count != 15:
                issues.append(f"public_table_count.expected_15_found_{table_count}")
            cur.execute("SELECT 1 FROM app_user WHERE role = 'EXPERT' AND is_active = TRUE LIMIT 1")
            if cur.fetchone() is None:
                issues.append("app_user.expert")
    return issues


@contextmanager
def get_connection() -> Generator:
    conn = psycopg2.connect(DB_CONFIG.dsn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_all(query: str, params: dict | None = None) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params or {})
            return list(cur.fetchall())


def fetch_one(query: str, params: dict | None = None) -> dict | None:
    rows = fetch_all(query, params)
    return rows[0] if rows else None


def execute(query: str, params: dict | None = None) -> int | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or {})
            if cur.description:
                row = cur.fetchone()
                return row[0] if row else None
            return cur.rowcount
