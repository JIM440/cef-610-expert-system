from app.database import execute, fetch_all, fetch_one, get_connection
from app.utils.passwords import hash_password


def _user_select() -> str:
    return """
        SELECT u.id, u.username, u.full_name, u.farmer_id, u.is_active,
               r.code AS role_code, r.label AS role_label
        FROM app_user u
        JOIN role r ON r.id = u.role_id
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
    row = fetch_one(
        "SELECT 1 AS ok FROM app_user WHERE username = %(username)s",
        {"username": username},
    )
    return row is not None


def get_role_id(role_code: str) -> int | None:
    row = fetch_one(
        "SELECT id FROM role WHERE code = %(code)s",
        {"code": role_code},
    )
    return row["id"] if row else None


def create_app_user(
    username: str,
    password: str,
    role_code: str,
    full_name: str,
    farmer_id: int | None = None,
) -> int:
    role_id = get_role_id(role_code)
    if not role_id:
        raise ValueError(f"Unknown role: {role_code}")
    return execute(
        """
        INSERT INTO app_user (username, password_hash, role_id, farmer_id, full_name)
        VALUES (%(username)s, %(password_hash)s, %(role_id)s, %(farmer_id)s, %(full_name)s)
        RETURNING id
        """,
        {
            "username": username,
            "password_hash": hash_password(password),
            "role_id": role_id,
            "farmer_id": farmer_id,
            "full_name": full_name,
        },
    )




def get_all_experts() -> list[dict]:
    return fetch_all(
        """
        SELECT u.id, u.username, u.full_name, u.created_at,
               r.code AS role_code, r.label AS role_label
        FROM app_user u
        JOIN role r ON r.id = u.role_id
        WHERE r.code = 'expert'
          AND u.is_active = TRUE
        ORDER BY u.full_name, u.username
        """
    )


def create_expert_account(full_name: str, username: str, password: str) -> int:
    if username_exists(username):
        raise ValueError(f"Username '{username}' is already taken.")
    return create_app_user(
        username=username,
        password=password,
        role_code="expert",
        full_name=full_name,
    )

def get_all_farmers() -> list[dict]:
    return fetch_all(
        """
        SELECT f.id, f.full_name, f.phone_number, f.location, f.email, f.created_at,
               u.username
        FROM farmer f
        LEFT JOIN app_user u ON u.farmer_id = f.id
        ORDER BY f.full_name
        """
    )


def create_farmer_record(full_name: str, phone: str, location: str, email: str) -> int:
    return execute(
        """
        INSERT INTO farmer (full_name, phone_number, location, email)
        VALUES (%(name)s, %(phone)s, %(location)s, %(email)s)
        RETURNING id
        """,
        {"name": full_name, "phone": phone, "location": location, "email": email},
    )


def create_farmer_with_account(
    full_name: str,
    phone: str,
    location: str,
    email: str,
    username: str,
    password: str,
) -> int:
    if username_exists(username):
        raise ValueError(f"Username '{username}' is already taken.")
    farmer_id = create_farmer_record(full_name, phone, location, email)
    create_app_user(username, password, "farmer", full_name, farmer_id=farmer_id)
    return farmer_id


def update_farmer_record(
    farmer_id: int, full_name: str, phone: str, location: str, email: str
) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE farmer
                SET full_name = %s, phone_number = %s, location = %s,
                    email = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """,
                (full_name, phone, location, email, farmer_id),
            )
            cur.execute(
                "UPDATE app_user SET full_name = %s WHERE farmer_id = %s",
                (full_name, farmer_id),
            )


def get_farmer_by_id(farmer_id: int) -> dict | None:
    return fetch_one(
        "SELECT id, full_name, phone_number, location, email FROM farmer WHERE id = %(id)s",
        {"id": farmer_id},
    )
