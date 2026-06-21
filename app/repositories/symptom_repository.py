from app.database import execute, fetch_all


def get_all_symptoms() -> list[dict]:
    return fetch_all("SELECT id, name, description FROM symptom ORDER BY name")


def create_symptom(name: str, description: str) -> int:
    return execute(
        """
        INSERT INTO symptom (name, description) VALUES (%(name)s, %(desc)s)
        RETURNING id
        """,
        {"name": name, "desc": description},
    )


def update_symptom(symptom_id: int, name: str, description: str) -> None:
    execute(
        """
        UPDATE symptom SET name = %(name)s, description = %(desc)s
        WHERE id = %(id)s
        """,
        {"id": symptom_id, "name": name, "desc": description},
    )


def delete_symptom(symptom_id: int) -> None:
    execute("DELETE FROM symptom WHERE id = %(id)s", {"id": symptom_id})


def get_environmental_conditions() -> list[dict]:
    return fetch_all(
        """
        SELECT
            ec.id AS condition_id,
            ec.name AS condition_name,
            ec.unit,
            ecv.id AS value_id,
            ecv.value_name
        FROM environmental_condition ec
        JOIN environmental_condition_value ecv ON ecv.condition_id = ec.id
        ORDER BY ec.name, ecv.value_name
        """
    )
