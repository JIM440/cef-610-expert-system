import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.disease_repository import get_all_diseases
from app.repositories.rule_repository import (
    create_rule,
    get_all_rules,
    link_rule_environment,
    link_rule_symptom,
    link_rule_treatment,
    update_rule_active,
)
from app.repositories.symptom_repository import get_all_symptoms, get_environmental_conditions
from app.repositories.treatment_repository import get_all_treatments
from app.utils.auth import require_admin

require_admin()
st.header("Expert Rules - Reasoning Layer")
st.caption(
    "Rule knowledge answers: When should the system diagnose this disease? "
    "Only symptoms required for diagnosis belong here."
)

rules = get_all_rules()
filter_text = st.text_input("Search rules", placeholder="Disease, rule name, status...")
if filter_text:
    q = filter_text.lower()
    rules = [
        r for r in rules
        if q in str(r.get("rule_name", "")).lower()
        or q in str(r.get("disease_name", "")).lower()
        or q in str(r.get("active_status", "")).lower()
    ]

st.subheader("Rule list")
if rules:
    df = pd.DataFrame(rules)
    st.dataframe(
        df[["id", "rule_name", "disease_name", "confidence_score", "active_status"]],
        width="stretch",
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "rule_name": "Rule",
            "disease_name": "Disease",
            "confidence_score": st.column_config.ProgressColumn(
                "Confidence", min_value=0, max_value=100, format="%d%%"
            ),
            "active_status": "Status",
        },
    )
    with st.expander("Toggle rule active status", expanded=False):
        rid = st.selectbox(
            "Rule",
            [r["id"] for r in rules],
            format_func=lambda i: next(r["rule_name"] for r in rules if r["id"] == i),
        )
        current = next(r["is_active"] for r in rules if r["id"] == rid)
        active = st.toggle("Active", value=bool(current))
        if st.button("Save rule status", type="primary"):
            update_rule_active(rid, active)
            st.success("Rule status updated.")
            st.rerun()
else:
    st.info("No rules match this filter.")

with st.expander("Create rule", expanded=False):
    diseases = get_all_diseases()
    disease_id = st.selectbox(
        "Disease",
        [d["id"] for d in diseases],
        format_func=lambda i: next(d["name"] for d in diseases if d["id"] == i),
    )
    rule_name = st.text_input("Rule name")
    confidence = st.slider("Confidence score", 0, 100, 75)

    symptoms = get_all_symptoms()
    selected_symptoms = st.multiselect("Required symptoms", [s["name"] for s in symptoms])
    symptom_map = {s["name"]: s["id"] for s in symptoms}

    env_rows = get_environmental_conditions()
    env_options = {
        f"{r['condition_name']}: {r['value_name']}": r["value_id"] for r in env_rows
    }
    selected_env = st.multiselect("Required conditions", list(env_options.keys()))

    treatments = get_all_treatments()
    selected_treatments = st.multiselect("Recommended treatments", [t["name"] for t in treatments])
    treatment_map = {t["name"]: t["id"] for t in treatments}

    if st.button("Create rule", type="primary"):
        if not rule_name or not selected_symptoms:
            st.error("Rule name and at least one symptom are required.")
        else:
            rule_id = create_rule(disease_id, rule_name, confidence)
            for sname in selected_symptoms:
                link_rule_symptom(rule_id, symptom_map[sname])
            for ename in selected_env:
                link_rule_environment(rule_id, env_options[ename])
            for i, tname in enumerate(selected_treatments, start=1):
                link_rule_treatment(rule_id, treatment_map[tname], i)
            st.success(f"Rule created (ID {rule_id}).")
            st.rerun()
