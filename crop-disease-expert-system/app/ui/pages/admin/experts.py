import app.path_setup  # noqa: F401

import streamlit as st

from app.repositories.user_repository import create_expert_account, get_all_experts
from app.ui.components.farmer_theme import render_page_header
from app.utils.auth import require_expert

require_expert()
render_page_header("Experts", "View and add crop expert accounts stored in the database.")

experts = get_all_experts()
list_tab, add_tab = st.tabs(["Expert cards", "+ Add expert"])

with list_tab:
    search = st.text_input("Search experts", placeholder="Name or username...")
    query = search.casefold().strip()
    filtered = [
        expert
        for expert in experts
        if not query
        or query in (expert.get("full_name") or "").casefold()
        or query in expert["username"].casefold()
    ]

    if not filtered:
        st.info("No experts match this search.")

    for start in range(0, len(filtered), 3):
        columns = st.columns(3)
        for column, expert in zip(columns, filtered[start : start + 3]):
            with column:
                with st.container(border=True):
                    st.subheader(expert.get("full_name") or expert["username"])
                    st.caption(f"@{expert['username']}")
                    st.write(f"**Role:** {expert['role_label']}")
                    created = expert.get("created_at")
                    registered = (
                        created.strftime("%b %d, %Y")
                        if hasattr(created, "strftime")
                        else str(created)[:10]
                    )
                    st.caption(f"Registered {registered}")

with add_tab:
    with st.form("add_expert_form"):
        full_name = st.text_input("Full name")
        username = st.text_input("Username", placeholder="Unique login name")
        password = st.text_input("Password", type="password")
        add = st.form_submit_button("Add expert", type="primary", width="stretch")

    if add:
        if not all([full_name.strip(), username.strip(), password]):
            st.error("Full name, username, and password are required.")
        else:
            try:
                create_expert_account(
                    full_name=full_name.strip(),
                    username=username.strip(),
                    password=password,
                )
                st.success(f"Expert account '{username.strip()}' created.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not create expert: {exc}")
