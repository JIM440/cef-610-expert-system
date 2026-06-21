import streamlit as st

from app.repositories.disease_repository import get_symptoms_for_disease
from app.ui.components.diagnosis_results_view import render_diagnosis_results_cards


def render_diagnosis_result(result: dict) -> None:
    render_diagnosis_results_cards(result)

    disease_id = result.get("disease_id")
    if not disease_id:
        return

    common = get_symptoms_for_disease(disease_id)
    matched_names = set(result.get("reasons", {}).get("symptoms", []))
    if common:
        with st.expander("Disease knowledge facts", expanded=False):
            for s in common:
                marker = "observed" if s["name"] in matched_names else "associated, not required for matched rule"
                st.write(f"- {s['name']} - {marker}")
