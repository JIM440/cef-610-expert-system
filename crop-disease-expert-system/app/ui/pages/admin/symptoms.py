import app.path_setup  # noqa: F401

import streamlit as st

from app.repositories.symptom_repository import create_symptom, delete_symptom, get_all_symptoms, update_symptom
from app.ui.components.farmer_theme import render_page_header
from app.utils.auth import require_expert

require_expert()
render_page_header("Symptoms", "Database symptom catalog used by Gemini mapping and expert rules.")
symptoms = get_all_symptoms()
list_tab, edit_tab, add_tab = st.tabs(["Symptom cards", "Edit symptom", "+ Add symptom"])

with list_tab:
    search = st.text_input("Search symptoms", placeholder="Name or description...")
    q = search.casefold().strip()
    filtered = [s for s in symptoms if not q or q in s["name"].casefold() or q in (s.get("description") or "").casefold()]
    for start in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, symptom in zip(cols, filtered[start:start + 3]):
            with col:
                with st.container(border=True):
                    st.subheader(symptom["name"])
                    st.write(symptom.get("description") or "No description provided.")
                    st.caption(f"Symptom ID {symptom['id']}")
    if not filtered:
        st.info("No symptoms match this search.")

with edit_tab:
    if symptoms:
        sid = st.selectbox("Select symptom", [s["id"] for s in symptoms], format_func=lambda i: next(s["name"] for s in symptoms if s["id"] == i))
        symptom = next(s for s in symptoms if s["id"] == sid)
        with st.form("edit_symptom_form"):
            name = st.text_input("Name", value=symptom["name"])
            description = st.text_area("Description", value=symptom.get("description") or "", height=140)
            save = st.form_submit_button("Save symptom", type="primary", width="stretch")
        if save:
            update_symptom(sid, name.strip(), description.strip())
            st.success("Symptom updated.")
            st.rerun()
        confirm = st.checkbox("I understand this may affect disease and rule links.")
        if st.button("Delete symptom", disabled=not confirm):
            delete_symptom(sid)
            st.success("Symptom deleted.")
            st.rerun()
    else:
        st.info("Add a symptom first.")

with add_tab:
    with st.form("add_symptom_form"):
        name = st.text_input("Symptom name")
        description = st.text_area("Description", height=140)
        add = st.form_submit_button("Add symptom", type="primary", width="stretch")
    if add:
        if not name.strip():
            st.error("Symptom name is required.")
        else:
            create_symptom(name.strip(), description.strip())
            st.success("Symptom added.")
            st.rerun()