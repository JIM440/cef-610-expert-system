import streamlit as st

from app.ui.theme import confidence_chip, escape
from app.utils.helpers import format_confidence


def render_diagnosis_results_cards(
    result: dict,
    show_saved_note: bool = True,
    saved_note: str = "Diagnosis saved to history automatically.",
) -> None:
    confidence = result.get("confidence", 0)
    match_tier = result.get("match_tier", "HIGH")
    tier_label = "Low confidence - possible match" if match_tier == "LOW" else "Expert rule match"
    reasons = result.get("reasons", {})

    st.markdown(
        f"""
        <div class="result-card">
            <div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;flex-wrap:wrap;">
                <div>
                    <div style="color:var(--muted);font-size:.82rem;font-weight:800;text-transform:uppercase;">Detected disease</div>
                    <div class="disease-name">{escape(result.get("disease_name", "-"))}</div>
                    <div style="margin-top:.35rem;color:var(--muted);">{escape(tier_label)}</div>
                </div>
                <div style="text-align:right;min-width:180px;">
                    {confidence_chip(confidence)}
                    <div style="margin-top:.55rem;color:var(--muted);font-size:.82rem;">Confidence score</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(min(max(confidence, 0), 100) / 100)
    st.caption(format_confidence(confidence))

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**Why this diagnosis**")
            symptom_lines = reasons.get("symptoms", [])
            condition_lines = reasons.get("conditions", [])
            if not symptom_lines and not condition_lines:
                st.caption("No matched rule details were returned.")
            for symptom in symptom_lines:
                st.write(f"- {symptom}")
            for condition in condition_lines:
                st.write(f"- {condition}")
            rule = reasons.get("rule")
            if rule:
                st.caption(f"Rule: {rule['rule_name']} ({rule['matched_score']}%)")

    with col2:
        with st.container(border=True):
            st.markdown("**Recommended treatments**")
            treatments = result.get("treatments", [])
            if not treatments:
                st.caption("No treatments linked to this rule yet.")
            for t in treatments:
                st.checkbox(
                    t["name"],
                    value=False,
                    disabled=True,
                    key=f"treat_{result.get('consultation_id')}_{t['id']}",
                )
                if t.get("description"):
                    st.caption(t["description"])

    with st.container(border=True):
        st.markdown("**Explanation**")
        st.write(result.get("explanation", ""))

    if show_saved_note:
        st.success(saved_note)
