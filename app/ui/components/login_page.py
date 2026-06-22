import streamlit as st

from app.repositories.user_repository import authenticate
from app.utils.auth import login_user


def render_login_page() -> None:
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stMainBlockContainer"] {
                width: 100%;
                max-width: 660px;
                margin-left: auto;
                margin-right: auto;
                box-sizing: border-box;
                padding-top: 12vh;
            }
            [data-testid="stMainBlockContainer"] h1,
            [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] {
                text-align: center;
            }
            [data-testid="stMainBlockContainer"] [data-testid="stForm"],
            [data-testid="stMainBlockContainer"] [data-testid="stTextInput"] {
                width: 100%;
                max-width: 500px;
                margin-left: auto;
                margin-right: auto;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Crop Disease Expert System")
    st.caption("Farmers and experts - sign in to continue")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login", type="primary", width="stretch")

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
