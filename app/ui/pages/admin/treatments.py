import app.path_setup  # noqa: F401

import streamlit as st

from app.repositories.treatment_repository import create_treatment, delete_treatment, get_all_treatments, update_treatment
from app.ui.components.farmer_theme import render_page_header
from app.utils.auth import require_expert

require_expert()
render_page_header("Treatments", "Treatment catalog referenced by diseases and expert rules.")
treatments = get_all_treatments()
list_tab, edit_tab, add_tab = st.tabs(["Treatment cards", "Edit treatment", "+ Add treatment"])

with list_tab:
    search = st.text_input("Search treatments", placeholder="Name or description...")
    q = search.casefold().strip()
    filtered = [t for t in treatments if not q or q in t["name"].casefold() or q in (t.get("description") or "").casefold()]
    for start in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, treatment in zip(cols, filtered[start:start + 3]):
            with col:
                with st.container(border=True):
                    st.subheader(treatment["name"])
                    st.write(treatment.get("description") or "No description provided.")
                    st.caption(f"Treatment ID {treatment['id']}")
    if not filtered:
        st.info("No treatments match this search.")

with edit_tab:
    if treatments:
        tid = st.selectbox("Select treatment", [t["id"] for t in treatments], format_func=lambda i: next(t["name"] for t in treatments if t["id"] == i))
        treatment = next(t for t in treatments if t["id"] == tid)
        with st.form("edit_treatment_form"):
            name = st.text_input("Name", value=treatment["name"])
            description = st.text_area("Description", value=treatment.get("description") or "", height=160)
            save = st.form_submit_button("Save treatment", type="primary", width="stretch")
        if save:
            update_treatment(tid, name.strip(), description.strip())
            st.success("Treatment updated.")
            st.rerun()
        confirm = st.checkbox("I understand this may affect disease and rule links.")
        if st.button("Delete treatment", disabled=not confirm):
            delete_treatment(tid)
            st.success("Treatment deleted.")
            st.rerun()
    else:
        st.info("Add a treatment first.")

with add_tab:
    with st.form("add_treatment_form"):
        name = st.text_input("Treatment name")
        description = st.text_area("Description", height=160)
        add = st.form_submit_button("Add treatment", type="primary", width="stretch")
    if add:
        if not name.strip():
            st.error("Treatment name is required.")
        else:
            create_treatment(name.strip(), description.strip())
            st.success("Treatment added.")
            st.rerun()