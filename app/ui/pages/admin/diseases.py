import app.path_setup  # noqa: F401

import streamlit as st

from app.repositories.crop_repository import get_tomato_crop_id
from app.repositories.disease_repository import (
    create_disease,
    delete_disease,
    get_all_diseases,
    get_disease_knowledge_summary,
    link_disease_symptom,
    link_disease_treatment,
    unlink_disease_symptom,
    update_disease,
)
from app.repositories.symptom_repository import get_all_symptoms
from app.repositories.treatment_repository import get_all_treatments
from app.ui.components.farmer_theme import render_page_header
from app.utils.auth import require_expert

require_expert()
render_page_header("Diseases", "Factual tomato disease knowledge used by experts and diagnosis reports.")
diseases = get_all_diseases()
list_tab, edit_tab, add_tab = st.tabs(["Disease cards", "Edit disease", "+ Add disease"])

with list_tab:
    search = st.text_input("Search diseases", placeholder="Name, description, symptom, or treatment...")
    q = search.casefold().strip()
    cards = []
    for disease in diseases:
        summary = get_disease_knowledge_summary(disease["id"])
        haystack = " ".join([
            disease["name"], disease.get("description") or "",
            " ".join(s["name"] for s in summary["symptoms"]),
            " ".join(t["name"] for t in summary["treatments"]),
        ]).casefold()
        if not q or q in haystack:
            cards.append(summary)
    for start in range(0, len(cards), 2):
        cols = st.columns(2)
        for col, summary in zip(cols, cards[start:start + 2]):
            disease = summary["disease"]
            with col:
                with st.container(border=True):
                    st.subheader(disease["name"])
                    st.write(disease.get("description") or "No description provided.")
                    st.markdown("**Common symptoms**")
                    st.caption(", ".join(s["name"] for s in summary["symptoms"]) or "None linked")
                    st.markdown("**Treatments**")
                    st.caption(", ".join(t["name"] for t in summary["treatments"]) or "None linked")
                    st.caption(f"Disease ID {disease['id']}")
    if not cards:
        st.info("No diseases match this search.")

with edit_tab:
    if not diseases:
        st.info("Add a disease first.")
    else:
        did = st.selectbox("Select disease", [d["id"] for d in diseases], format_func=lambda i: next(d["name"] for d in diseases if d["id"] == i))
        summary = get_disease_knowledge_summary(did)
        disease = summary["disease"]
        with st.form("edit_disease_form"):
            name = st.text_input("Name", value=disease["name"])
            description = st.text_area("Description", value=disease.get("description") or "", height=130)
            template = st.text_area("Diagnosis explanation template", value=disease.get("explanation_template") or "", height=130)
            save = st.form_submit_button("Save disease", type="primary", width="stretch")
        if save:
            update_disease(did, name.strip(), description.strip(), template.strip())
            st.success("Disease updated.")
            st.rerun()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Symptom associations**")
            for symptom in summary["symptoms"]:
                st.write(f"- {symptom['name']} (weight {symptom['weight']})")
            all_symptoms = get_all_symptoms()
            linked_ids = {s["id"] for s in summary["symptoms"]}
            available = [s for s in all_symptoms if s["id"] not in linked_ids]
            if available:
                sid = st.selectbox("Add symptom", [s["id"] for s in available], format_func=lambda i: next(s["name"] for s in available if s["id"] == i))
                weight = st.number_input("Association weight", min_value=1, max_value=10, value=1)
                if st.button("Link symptom"):
                    link_disease_symptom(did, sid, weight)
                    st.rerun()
            if summary["symptoms"]:
                remove_sid = st.selectbox("Remove symptom", [s["id"] for s in summary["symptoms"]], format_func=lambda i: next(s["name"] for s in summary["symptoms"] if s["id"] == i))
                if st.button("Unlink symptom"):
                    unlink_disease_symptom(did, remove_sid)
                    st.rerun()
        with c2:
            st.markdown("**Treatment associations**")
            for treatment in summary["treatments"]:
                st.write(f"- {treatment['name']}")
            all_treatments = get_all_treatments()
            linked_treatments = {t["id"] for t in summary["treatments"]}
            available_treatments = [t for t in all_treatments if t["id"] not in linked_treatments]
            if available_treatments:
                tid = st.selectbox("Add treatment", [t["id"] for t in available_treatments], format_func=lambda i: next(t["name"] for t in available_treatments if t["id"] == i))
                priority = st.number_input("Treatment priority", min_value=1, max_value=5, value=1)
                if st.button("Link treatment"):
                    link_disease_treatment(did, tid, priority)
                    st.rerun()
            st.markdown("**Environmental facts**")
            for environment in summary["environments"]:
                st.write(f"- {environment['condition_name']}: {environment['value_name']}")

        confirm = st.checkbox("I understand deleting this disease also removes its linked rules.")
        if st.button("Delete disease", disabled=not confirm):
            delete_disease(did)
            st.success("Disease deleted.")
            st.rerun()

with add_tab:
    crop_id = get_tomato_crop_id()
    if crop_id is None:
        st.warning("Tomato crop is not configured in the database.")
    else:
        with st.form("add_disease_form"):
            name = st.text_input("Disease name")
            description = st.text_area("Description", height=130)
            template = st.text_area("Diagnosis explanation template", height=130)
            add = st.form_submit_button("Add disease", type="primary", width="stretch")
        if add:
            if not name.strip():
                st.error("Disease name is required.")
            else:
                create_disease(crop_id, name.strip(), description.strip(), template.strip())
                st.success("Disease added. Use Edit disease to link symptoms and treatments.")
                st.rerun()