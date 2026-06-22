from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extras

from app.config import DB_CONFIG

REQUIRED_SCHEMA_COLUMNS = {
    "consultation": {"source", "gemini_raw_extraction", "match_tier"},
    "consultation_symptom": {"matched"},
    "consultation_environment": {"matched"},
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
            cur.execute("SELECT 1 FROM role WHERE code = 'expert'")
            if cur.fetchone() is None:
                issues.append("role.expert")
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
