def format_confidence(score: int | None) -> str:
    if score is None:
        return "N/A"
    return f"{score}%"
