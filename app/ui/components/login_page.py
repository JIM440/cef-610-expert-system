import streamlit as st

from app.repositories.user_repository import authenticate
from app.utils.auth import login_user


def render_login_page() -> None:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none; }
            .main .block-container {
                max-width: 400px;
                padding-top: 12vh;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Crop Disease Expert System")
    st.caption("Farmers and experts — sign in to continue")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

    if submitted:
        if not username.strip() or not password:
            st.error("Please enter both username and password.")
            return
        try:
            account = authenticate(username.strip(), password)
        except Exception as exc:
            st.error(f"Login failed: {exc}")
            return
        if account:
            login_user(dict(account))
            st.rerun()
        st.error("Invalid username or password.")
