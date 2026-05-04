def validate_non_empty(v: str) -> str:
    if isinstance(v, str) and not v.strip():
        raise ValueError("The field cannot be empty or contain only spaces")
    return v.strip() if isinstance(v, str) else v
