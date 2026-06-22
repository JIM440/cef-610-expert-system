import app.path_setup  # noqa: F401 - project root on sys.path

import streamlit as st

from app.database import get_schema_issues, test_connection
from app.ui.components.login_page import render_login_page
from app.ui.theme import configure_page, inject_theme
from app.utils.auth import current_user, ensure_authenticated, init_session, is_expert, logout_user

configure_page()
init_session()

connection_ok, connection_error = test_connection()
if not connection_ok:
    st.error(f"Cannot connect to the database: {connection_error}")
    st.caption("Check `.env` and run `database/run_all.sql` for a new database.")
    st.stop()

schema_issues = get_schema_issues()
if schema_issues:
    st.error("The database schema is out of date.")
    st.code("python scripts/apply_schema_updates.py")
    st.caption("Missing columns: " + ", ".join(schema_issues))
    st.stop()

if not current_user():
    render_login_page()
    st.stop()

user = ensure_authenticated()
if not user:
    render_login_page()
    st.stop()

inject_theme()

with st.sidebar:
    if st.button("Log out", width="stretch"):
        logout_user()
        st.rerun()
farmer_pages = [
    st.Page("pages/farmer/dashboard.py", title="Dashboard", icon="🏠"),
    st.Page("pages/farmer/diagnosis.py", title="Diagnosis", icon="🩺"),
    st.Page("pages/farmer/my_history.py", title="History", icon="📋"),
    st.Page("pages/farmer/image_recognition.py", title="Image Recognition", icon="📷"),
]

if is_expert():
    pages = {
        "Diagnosis workspace": [
            st.Page("pages/admin/dashboard.py", title="Dashboard", icon="🏠"),
            st.Page("pages/admin/diagnosis.py", title="Diagnosis", icon="🩺"),
            st.Page("pages/admin/history.py", title="History", icon="📋"),
            st.Page("pages/admin/image_recognition.py", title="Image Recognition", icon="📷"),
        ],
        "Expert-only": [
            st.Page("pages/admin/experts.py", title="Experts", icon="👤"),
            st.Page("pages/admin/farmers.py", title="Farmers", icon="👥"),
            st.Page("pages/admin/diseases.py", title="Diseases", icon="🍅"),
            st.Page("pages/admin/symptoms.py", title="Symptoms", icon="🍃"),
            st.Page("pages/admin/treatments.py", title="Treatments", icon="💊"),
            st.Page("pages/admin/rules.py", title="Expert Rules", icon="🧠"),
        ],
    }
else:
    pages = {"My workspace": farmer_pages}
pg = st.navigation(pages)
pg.run()
