import pandas as pd
import streamlit as st

from app.repositories.user_repository import get_all_farmers
from app.services.consultation_service import ConsultationService
from app.ui.components.farmer_theme import render_page_header
from app.utils.consultation_types import LABELS


def _format_date(value) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%b %d, %Y %H:%M")
    return str(value)[:16]


def _result_text(disease: str | None, confidence: int | None) -> str:
    if not disease:
        return "No result"
    return f"{disease} ({int(confidence or 0)}%)"


def _agreement_text(value) -> str:
    if value is True:
        return "Agree"
    if value is False:
        return "Disagree"
    return "Unavailable"


def _history_dataframe(history: list[dict], show_farmer: bool) -> pd.DataFrame:
    rows = []
    for row in history:
        entry = {
            "Date": _format_date(row["consultation_date"]),
            "Rule-Based Result": _result_text(
                row.get("diagnosed_disease"), row.get("confidence_score")
            ),
            "AI Prediction": _result_text(
                row.get("ai_predicted_disease"), row.get("ai_confidence")
            ),
            "Agreement": _agreement_text(row.get("methods_agree")),
            "Symptoms": row.get("symptoms") or "-",
            "Source": "Image recognition" if row.get("source") == "IMAGE" else "Manual selection",
        }
        if show_farmer:
            entry["Farmer"] = row.get("farmer_name") or "General consultation"
            entry["Type"] = LABELS.get(row.get("consultation_type"), row.get("consultation_type", "-"))
        rows.append(entry)

    columns = ["Date"]
    if show_farmer:
        columns.append("Farmer")
    columns.extend(["Rule-Based Result", "AI Prediction", "Agreement", "Symptoms", "Source"])
    if show_farmer:
        columns.append("Type")
    return pd.DataFrame(rows)[columns]


def _format_history_report(history: list[dict], scope_label: str) -> str:
    lines = [
        "TOMATO DISEASE CONSULTATION REPORT",
        f"Scope: {scope_label}",
        f"Consultations: {len(history)}",
        "",
    ]
    for index, row in enumerate(history, start=1):
        lines.extend(
            [
                "=" * 72,
                f"CONSULTATION {index}",
                "=" * 72,
                f"Date: {_format_date(row.get('consultation_date'))}",
                f"Farmer: {row.get('farmer_name') or 'General consultation'}",
                f"Performed by: {row.get('performed_by_name') or row.get('performed_by') or '-'}",
                f"Crop: {row.get('crop_name') or '-'}",
                f"Source: {'Image recognition' if row.get('source') == 'IMAGE' else 'Manual symptom selection'}",
                f"Consultation type: {LABELS.get(row.get('consultation_type'), row.get('consultation_type') or '-')}",
                "",
                "RULE-BASED RESULT",
                f"Disease: {row.get('diagnosed_disease') or 'No rule-based diagnosis'}",
                f"Confidence: {int(row.get('confidence_score') or 0)}%",
                f"Match tier: {row.get('match_tier') or 'NONE'}",
                f"Explanation: {row.get('explanation') or '-'}",
                "",
                "AI PREDICTION (NAIVE BAYES)",
                f"Disease: {row.get('ai_predicted_disease') or 'No AI prediction'}",
                f"Confidence: {int(row.get('ai_confidence') or 0)}%",
                f"Model version: {row.get('ai_model_version') or '-'}",
                f"Agreement: {_agreement_text(row.get('methods_agree'))}",
                "",
                f"Submitted symptoms: {row.get('symptoms') or '-'}",
                f"Proposed treatments: {row.get('treatments') or '-'}",
            ]
        )
        if row.get("gemini_raw_extraction"):
            lines.extend(["", "Gemini extraction:", row["gemini_raw_extraction"]])
        lines.append("")
    return "\n".join(lines).strip()


def render_consultation_history_page(
    farmer_id: int | None = None,
    allow_farmer_filter: bool = False,
    page_title: str = "My History",
) -> None:
    render_page_header(
        page_title,
        "Review rule-based and Naive Bayes results, then edit and export the filtered consultations.",
    )

    service = ConsultationService()
    selected_farmer_id = farmer_id
    selected_farmer_label = "My consultations"
    col1, col2 = st.columns([1, 1])
    with col1:
        source_filter = st.radio(
            "Source",
            ["All diagnoses", "Manual diagnosis", "Image recognition"],
            index=0,
            horizontal=True,
        )
    diagnosis_source = {
        "All diagnoses": "all",
        "Manual diagnosis": "symptom",
        "Image recognition": "image",
    }[source_filter]

    show_farmer = allow_farmer_filter
    if allow_farmer_filter:
        with col2:
            farmers = get_all_farmers()
            options: dict[str, int | None] = {"All farmers": None}
            options.update({f["full_name"]: f["id"] for f in farmers})
            choice = st.selectbox("Farmer", list(options), index=0)
            selected_farmer_id = options[choice]
            selected_farmer_label = choice

    history = service.get_history(
        farmer_id=selected_farmer_id,
        diagnosis_source=diagnosis_source,
    )
    if not history:
        st.info("No consultations found for this filter.")
        return

    history_tab, export_tab = st.tabs(["Consultations", "Export PDF"])
    with history_tab:
        df = _history_dataframe(history, show_farmer=show_farmer)
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            height=min(600, 90 + len(df) * 38),
            column_config={
                "Symptoms": st.column_config.TextColumn("Submitted symptoms", width="large"),
                "Rule-Based Result": st.column_config.TextColumn(width="medium"),
                "AI Prediction": st.column_config.TextColumn(width="medium"),
            },
        )

    with export_tab:
        scope = f"{selected_farmer_label}; source: {source_filter}"
        default_content = _format_history_report(history, scope)
        editor_key = f"history_export_{selected_farmer_id}_{diagnosis_source}"
        edited_content = st.text_area(
            "Editable consultation report",
            value=default_content,
            height=560,
            key=editor_key,
            help="This single report contains every consultation in the current filter.",
        )
        if st.button("Generate PDF", type="primary", width="stretch", key=f"generate_{editor_key}"):
            st.session_state[f"pdf_{editor_key}"] = service.export_history_pdf(
                "Tomato Disease Consultation History",
                edited_content,
            )
            st.success("PDF generated from the edited consultation report.")

        pdf_bytes = st.session_state.get(f"pdf_{editor_key}")
        if pdf_bytes:
            st.download_button(
                "Download PDF report",
                data=pdf_bytes,
                file_name="consultation_history.pdf",
                mime="application/pdf",
                width="stretch",
                key=f"download_{editor_key}",
            )
