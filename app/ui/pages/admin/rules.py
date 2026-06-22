import app.path_setup  # noqa: F401

import streamlit as st

from app.repositories.disease_repository import get_all_diseases
from app.repositories.rule_repository import (
    create_rule,
    get_all_rules,
    get_rule_detail,
    link_rule_environment,
    link_rule_symptom,
    link_rule_treatment,
    update_rule,
)
from app.repositories.symptom_repository import get_all_symptoms, get_environmental_conditions
from app.repositories.treatment_repository import get_all_treatments
from app.ui.components.farmer_theme import render_page_header
from app.utils.auth import require_expert

require_expert()
render_page_header("Expert Rules", "Define and maintain the database rules used for final diagnosis.")

rules = get_all_rules()
diseases = get_all_diseases()
symptoms = get_all_symptoms()
environments = get_environmental_conditions()
treatments = get_all_treatments()

disease_names = {d["id"]: d["name"] for d in diseases}
symptom_names = {s["id"]: s["name"] for s in symptoms}
environment_names = {e["value_id"]: f"{e['condition_name']}: {e['value_name']}" for e in environments}
treatment_names = {t["id"]: t["name"] for t in treatments}


def confidence_level(value: int) -> str:
    return "High" if value >= 80 else "Moderate" if value >= 60 else "Low"


list_tab, edit_tab, create_tab = st.tabs(["Rule cards", "Edit rule", "+ Create rule"])

with list_tab:
    search = st.text_input("Search expert rules", placeholder="Rule, disease, symptom, condition, or treatment...")
    q = search.casefold().strip()
    filtered = [r for r in rules if not q or q in " ".join(str(r.get(k) or "") for k in ("rule_name", "disease_name", "symptoms", "conditions", "treatments")).casefold()]
    for start in range(0, len(filtered), 2):
        cols = st.columns(2)
        for col, rule in zip(cols, filtered[start:start + 2]):
            with col:
                with st.container(border=True):
                    st.subheader(rule["rule_name"])
                    st.caption(rule["disease_name"])
                    st.metric("Confidence", f"{rule['confidence_score']}%", confidence_level(rule["confidence_score"]))
                    st.markdown("**Required symptoms**")
                    st.write(rule.get("symptoms") or "-")
                    st.markdown("**Conditions**")
                    st.write(rule.get("conditions") or "-")
                    st.markdown("**Recommended treatments**")
                    st.write(rule.get("treatments") or "-")
    if not filtered:
        st.info("No rules match this search.")

with edit_tab:
    if not rules:
        st.info("Create a rule first.")
    else:
        rid = st.selectbox("Select rule", [r["id"] for r in rules], format_func=lambda i: next(r["rule_name"] for r in rules if r["id"] == i))
        detail = get_rule_detail(rid)
        with st.form("edit_rule_form"):
            disease_id = st.selectbox("Disease", list(disease_names), index=list(disease_names).index(detail["disease_id"]), format_func=lambda i: disease_names[i])
            rule_name = st.text_input("Rule name", value=detail["rule_name"])
            confidence = st.slider("Rule confidence", 0, 100, int(detail["confidence_score"]), help="High: 80-100, Moderate: 60-79, Low: below 60")
            st.caption(f"Confidence level: {confidence_level(confidence)}")
            selected_symptoms = st.multiselect("Required symptoms", list(symptom_names), default=detail["symptom_ids"], format_func=lambda i: symptom_names[i])
            selected_conditions = st.multiselect("Required environmental conditions", list(environment_names), default=detail["condition_value_ids"], format_func=lambda i: environment_names[i])
            selected_treatments = st.multiselect("Recommended treatments", list(treatment_names), default=detail["treatment_ids"], format_func=lambda i: treatment_names[i])
            save = st.form_submit_button("Save rule", type="primary", width="stretch")
        if save:
            if not rule_name.strip() or not selected_symptoms:
                st.error("Rule name and at least one required symptom are required.")
            else:
                update_rule(rid, disease_id, rule_name.strip(), confidence, selected_symptoms, selected_conditions, selected_treatments)
                st.success("Expert rule updated.")
                st.rerun()

with create_tab:
    with st.form("create_rule_form"):
        disease_id = st.selectbox("Disease", list(disease_names), format_func=lambda i: disease_names[i])
        rule_name = st.text_input("Rule name")
        confidence = st.slider("Rule confidence", 0, 100, 75, help="High: 80-100, Moderate: 60-79, Low: below 60")
        st.caption(f"Confidence level: {confidence_level(confidence)}")
        selected_symptoms = st.multiselect("Required symptoms", list(symptom_names), format_func=lambda i: symptom_names[i])
        selected_conditions = st.multiselect("Required environmental conditions", list(environment_names), format_func=lambda i: environment_names[i])
        selected_treatments = st.multiselect("Recommended treatments", list(treatment_names), format_func=lambda i: treatment_names[i])
        create = st.form_submit_button("Create rule", type="primary", width="stretch")
    if create:
        if not rule_name.strip() or not selected_symptoms:
            st.error("Rule name and at least one required symptom are required.")
        else:
            rule_id = create_rule(disease_id, rule_name.strip(), confidence)
            for sid in selected_symptoms:
                link_rule_symptom(rule_id, sid)
            for value_id in selected_conditions:
                link_rule_environment(rule_id, value_id)
            for priority, tid in enumerate(selected_treatments, start=1):
                link_rule_treatment(rule_id, tid, min(priority, 5))
            st.success(f"Expert rule created with ID {rule_id}.")
            st.rerun()