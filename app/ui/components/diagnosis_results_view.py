import streamlit as st

from app.ui.theme import confidence_chip, escape
from app.utils.helpers import format_confidence


def _result_panel(title: str, disease: str | None, confidence: int, subtitle: str) -> str:
    return f"""
        <div class="result-card" style="height:100%;">
            <div style="color:var(--muted);font-size:.82rem;font-weight:800;text-transform:uppercase;">{escape(title)}</div>
            <div class="disease-name" style="font-size:1.45rem;margin-top:.35rem;">{escape(disease or "No result")}</div>
            <div style="margin-top:.65rem;">{confidence_chip(confidence)}</div>
            <div style="margin-top:.55rem;color:var(--muted);font-size:.82rem;">{escape(subtitle)}</div>
        </div>
    """


def render_diagnosis_results_cards(
    result: dict,
    show_saved_note: bool = True,
    saved_note: str = "Diagnosis saved to history automatically.",
) -> None:
    rule_confidence = int(result.get("confidence") or 0)
    match_tier = result.get("match_tier", "NONE")
    tier_label = {
        "HIGH": "Complete expert-rule match",
        "LOW": "Partial expert-rule match",
        "NONE": "No expert rule matched",
    }.get(match_tier, "Expert-rule result")
    ai = result.get("ai_prediction") or {}
    ai_confidence = int(ai.get("confidence") or 0)

    rule_col, ai_col = st.columns(2)
    with rule_col:
        st.markdown(
            _result_panel(
                "Rule-Based Result",
                result.get("disease_name"),
                rule_confidence,
                tier_label,
            ),
            unsafe_allow_html=True,
        )
        st.progress(min(max(rule_confidence, 0), 100) / 100)
        st.caption(format_confidence(rule_confidence))

    with ai_col:
        st.markdown(
            _result_panel(
                "AI Prediction (Naive Bayes)",
                ai.get("disease_name"),
                ai_confidence,
                ai.get("model_version") or "No AI prediction",
            ),
            unsafe_allow_html=True,
        )
        st.progress(min(max(ai_confidence, 0), 100) / 100)
        st.caption(f"Normalized Naive Bayes probability: {ai_confidence}%")

    agreement = result.get("methods_agree")
    if agreement is True:
        st.success("Both methods agree on the predicted disease.")
    elif agreement is False:
        st.warning("Methods disagree. Review the rule evidence and AI probability independently.")
    else:
        st.info("Agreement is unavailable because one method did not return a disease.")

    reasons = result.get("reasons", {})
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**Why the rule-based method returned this result**")
            symptom_lines = reasons.get("symptoms", [])
            condition_lines = reasons.get("conditions", [])
            if not symptom_lines and not condition_lines:
                st.caption("No matched rule evidence was returned.")
            for symptom in symptom_lines:
                st.write(f"- {symptom}")
            for condition in condition_lines:
                st.write(f"- {condition}")
            rule = reasons.get("rule")
            if rule:
                st.caption(f"Rule: {rule['rule_name']} ({rule['matched_score']}%)")

    with col2:
        with st.container(border=True):
            st.markdown("**Proposed treatments**")
            treatments = result.get("treatments", [])
            if not treatments:
                st.caption("No treatments linked to the matched rule.")
            for treatment in treatments:
                st.markdown(f"**{escape(treatment['name'])}**")
                if treatment.get("description"):
                    st.caption(treatment["description"])

    with st.container(border=True):
        st.markdown("**Rule-based explanation**")
        st.write(result.get("explanation", ""))

    if show_saved_note:
        st.success(saved_note)
