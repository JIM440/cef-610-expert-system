from app.database import execute, fetch_all


def get_all_treatments() -> list[dict]:
    return fetch_all(
        "SELECT id, name, description FROM treatment ORDER BY name"
    )


def create_treatment(name: str, description: str) -> int:
    return execute(
        """
        INSERT INTO treatment (name, description) VALUES (%(name)s, %(desc)s)
        RETURNING id
        """,
        {"name": name, "desc": description},
    )


def update_treatment(treatment_id: int, name: str, description: str) -> None:
    execute(
        """
        UPDATE treatment SET name = %(name)s, description = %(desc)s
        WHERE id = %(id)s
        """,
        {"id": treatment_id, "name": name, "desc": description},
    )


def delete_treatment(treatment_id: int) -> None:
    execute("DELETE FROM treatment WHERE id = %(id)s", {"id": treatment_id})
