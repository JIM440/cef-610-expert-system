def require_non_empty_selection(name: str, ids: list[int]) -> str | None:
    if not ids:
        return f"Please select at least one {name}."
    return None
