from app.database import execute, fetch_all, fetch_one, get_connection
from app.utils.passwords import hash_password


def _user_select() -> str:
    return """
        SELECT u.id, u.username, u.full_name, u.is_active,
               LOWER(u.role) AS role_code,
               INITCAP(LOWER(u.role)) AS role_label,
               CASE WHEN u.role = 'FARMER' THEN u.id END AS farmer_id,
               u.phone_number, u.location, u.email, u.created_at, u.updated_at
        FROM app_user u
    """


def authenticate(username: str, password: str) -> dict | None:
    return fetch_one(
        f"""
        {_user_select()}
        WHERE u.username = %(username)s
          AND u.password_hash = %(password_hash)s
          AND u.is_active = TRUE
        """,
        {"username": username, "password_hash": hash_password(password)},
    )


def get_user_by_id(user_id: int) -> dict | None:
    return fetch_one(
        f"{_user_select()} WHERE u.id = %(id)s AND u.is_active = TRUE",
        {"id": user_id},
    )


def username_exists(username: str) -> bool:
    return fetch_one(
        "SELECT 1 AS ok FROM app_user WHERE username = %(username)s",
        {"username": username},
    ) is not None


def create_app_user(
    username: str | None,
    password: str | None,
    role_code: str,
    full_name: str,
    phone_number: str | None = None,
    location: str | None = None,
    email: str | None = None,
) -> int:
    role = role_code.upper()
    if role not in {"ADMIN", "EXPERT", "FARMER"}:
        raise ValueError(f"Unknown role: {role_code}")
    if username and username_exists(username):
        raise ValueError(f"Username '{username}' is already taken.")
    return execute(
        """
        INSERT INTO app_user (
            username, password_hash, role, full_name,
            phone_number, location, email, updated_at
        )
        VALUES (
            %(username)s, %(password_hash)s, %(role)s, %(full_name)s,
            %(phone)s, %(location)s, %(email)s, CURRENT_TIMESTAMP
        )
        RETURNING id
        """,
        {
            "username": username or None,
            "password_hash": hash_password(password) if password else None,
            "role": role,
            "full_name": full_name,
            "phone": phone_number,
            "location": location,
            "email": email,
        },
    )


def get_all_experts() -> list[dict]:
    return fetch_all(
        """
        SELECT id, username, full_name, created_at,
               LOWER(role) AS role_code, INITCAP(LOWER(role)) AS role_label
        FROM app_user
        WHERE role = 'EXPERT' AND is_active = TRUE
        ORDER BY full_name, username
        """
    )


def create_expert_account(full_name: str, username: str, password: str) -> int:
    return create_app_user(username, password, "EXPERT", full_name)


def get_all_farmers() -> list[dict]:
    return fetch_all(
        """
        SELECT id, full_name, phone_number, location, email, created_at, username
        FROM app_user
        WHERE role = 'FARMER'
        ORDER BY full_name
        """
    )


def create_farmer_with_account(
    full_name: str,
    phone: str,
    location: str,
    email: str,
    username: str,
    password: str,
) -> int:
    return create_app_user(
        username, password, "FARMER", full_name,
        phone_number=phone, location=location, email=email,
    )


def update_farmer_record(
    farmer_id: int, full_name: str, phone: str, location: str, email: str
) -> None:
    execute(
        """
        UPDATE app_user
        SET full_name=%(name)s, phone_number=%(phone)s,
            location=%(location)s, email=%(email)s,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=%(id)s AND role='FARMER'
        """,
        {"id": farmer_id, "name": full_name, "phone": phone,
         "location": location, "email": email},
    )


def get_farmer_by_id(farmer_id: int) -> dict | None:
    return fetch_one(
        """
        SELECT id, full_name, phone_number, location, email, username
        FROM app_user WHERE id=%(id)s AND role='FARMER'
        """,
        {"id": farmer_id},
    )
