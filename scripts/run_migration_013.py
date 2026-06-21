from pathlib import Path

from app.database import get_connection, test_connection

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ok, err = test_connection()
    if not ok:
        raise SystemExit(f"DB connection failed: {err}")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'consultation_image'
                )
                """
            )
            exists = cur.fetchone()[0]
            if not exists:
                print("consultation_image not found — applying migration 012 first...")
                sql012 = (ROOT / "database/migrations/012_create_consultation_image_table.sql").read_text()
                cur.execute(sql012)
                print("Migration 012 applied.")

            sql013 = (ROOT / "database/migrations/013_alter_consultation_image_no_storage.sql").read_text()
            lines = [ln for ln in sql013.splitlines() if not ln.strip().startswith("--")]
            for stmt in "".join(lines).split(";"):
                stmt = stmt.strip()
                if stmt and not stmt.startswith("--"):
                    cur.execute(stmt)

            cur.execute(
                """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = 'consultation_image'
                ORDER BY ordinal_position
                """
            )
            cols = [r[0] for r in cur.fetchall()]

    print("Migration 013 complete.")
    print("consultation_image columns:", ", ".join(cols))


if __name__ == "__main__":
    main()
