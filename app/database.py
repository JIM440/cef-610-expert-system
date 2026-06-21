from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extras

from app.config import DB_CONFIG


def test_connection() -> tuple[bool, str]:
    try:
        with psycopg2.connect(DB_CONFIG.dsn, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return True, ""
    except Exception as exc:
        return False, str(exc)


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
