import streamlit as st

from app.repositories import user_repository as user_repo
from app.utils.passwords import hash_password  # noqa: F401 — re-export for callers


def init_session() -> None:
    if "user" not in st.session_state:
        st.session_state.user = None


def login_user(user: dict) -> None:
    st.session_state.user = dict(user)


def logout_user() -> None:
    st.session_state.user = None


def current_user() -> dict | None:
    user = st.session_state.get("user")
    return dict(user) if user else None


def is_admin() -> bool:
    user = current_user()
    return bool(user and user.get("role_code") == "admin")


def is_farmer() -> bool:
    user = current_user()
    return bool(user and user.get("role_code") == "farmer")


def ensure_authenticated() -> dict | None:
    """Re-validate session user against the database."""
    user = current_user()
    if not user:
        return None

    fresh = user_repo.get_user_by_id(user["id"])
    if not fresh or not fresh.get("is_active"):
        logout_user()
        return None

    login_user(fresh)
    return fresh


def require_login() -> dict:
    user = ensure_authenticated()
    if not user:
        st.warning("Please log in to continue.")
        st.stop()
    return user


def require_admin() -> dict:
    user = require_login()
    if user.get("role_code") != "admin":
        st.error("Access denied. Administrator account required.")
        st.stop()
    return user


def require_farmer() -> dict:
    user = require_login()
    if user.get("role_code") != "farmer":
        st.error("Access denied. Farmer account required.")
        st.stop()
    return user
