"""Apply idempotent schema updates required by the current application."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import get_connection, get_schema_issues, test_connection  # noqa: E402
MIGRATIONS = (
    "015_consultation_source_match_tier.sql",
    "016_consultation_match_trace.sql",
    "017_create_expert_role.sql",
)


def main() -> None:
    connected, error = test_connection()
    if not connected:
        raise SystemExit(f"Database connection failed: {error}")

    for filename in MIGRATIONS:
        path = ROOT / "database" / "migrations" / filename
        sql = path.read_text(encoding="utf-8-sig")
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
        print(f"Applied {filename}")

    issues = get_schema_issues()
    if issues:
        raise SystemExit("Schema is still missing: " + ", ".join(issues))
    print("Database schema is up to date.")


if __name__ == "__main__":
    main()