from pathlib import Path

from app.database import fetch_all, get_connection

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    sql = (ROOT / "database/migrations/014_image_consultation_types.sql").read_text()
    lines = [ln for ln in sql.splitlines() if not ln.strip().startswith("--")]
    statements = [s.strip() for s in "".join(lines).split(";") if s.strip()]

    with get_connection() as conn:
        with conn.cursor() as cur:
            for stmt in statements:
                print("Running:", stmt[:80] + ("..." if len(stmt) > 80 else ""))
                cur.execute(stmt)

    cols = fetch_all(
        """
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'consultation_image'
        ORDER BY ordinal_position
        """
    )
    print("Migration 014 complete.")
    print("consultation_image columns:", ", ".join(c["column_name"] for c in cols))


if __name__ == "__main__":
    main()
