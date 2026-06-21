import streamlit as st


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### Crop Disease Expert System")
        st.markdown("CEF610 Final Practical Project")
        st.markdown("---")
        st.caption("PostgreSQL · Rule Engine · Random Forest")
