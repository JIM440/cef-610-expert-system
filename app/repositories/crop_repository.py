from app.database import fetch_all, fetch_one

TOMATO_CROP_NAME = "Tomato"


def get_all_crops() -> list[dict]:
    return fetch_all("SELECT id, name, description FROM crop ORDER BY name")


def get_tomato_crop() -> dict | None:
    return fetch_one(
        "SELECT id, name, description FROM crop WHERE name = %(name)s",
        {"name": TOMATO_CROP_NAME},
    )


def get_tomato_crop_id() -> int | None:
    crop = get_tomato_crop()
    return crop["id"] if crop else None


def get_crop_by_id(crop_id: int) -> dict | None:
    return fetch_one(
        "SELECT id, name, description FROM crop WHERE id = %(id)s",
        {"id": crop_id},
    )
