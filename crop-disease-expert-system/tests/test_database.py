"""Database integration tests — require a running PostgreSQL instance."""

import pytest

from app.database import fetch_one


@pytest.mark.integration
def test_crop_table_exists():
    row = fetch_one("SELECT COUNT(*) AS count FROM crop")
    assert row is not None
    assert row["count"] >= 0
