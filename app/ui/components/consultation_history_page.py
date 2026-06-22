import pandas as pd
import streamlit as st

from app.repositories.user_repository import get_all_farmers
from app.services.consultation_service import ConsultationService
from app.ui.components.farmer_theme import render_page_header
from app.ui.components.history_export import render_history_detail, render_pdf_export_editor
from app.utils.consultation_types import LABELS


def _format_date(value) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%b %d, %Y")
    return str(value)[:10]


def _history_dataframe(history: list[dict], show_farmer: bool) -> pd.DataFrame:
    rows = []
    for row in history:
        entry = {
            "ID": row["consultation_id"],
            "Date": _format_date(row["consultation_date"]),
            "Disease": row["diagnosed_disease"] or "-",
            "Symptoms": row.get("symptoms") or "-",
            "Confidence": row.get("confidence_score") or 0,
            "Source": "Image recognition" if row.get("source") == "IMAGE" else "Manual selection",
            "Match": row.get("match_tier") or "HIGH",
        }
        if show_farmer:
            entry["Farmer"] = row.get("farmer_name") or "General consultation"
            entry["Type"] = LABELS.get(row.get("consultation_type"), row.get("consultation_type", "-"))
        rows.append(entry)

    columns = ["ID", "Date"]
    if show_farmer:
        columns.append("Farmer")
    columns.extend(["Disease", "Symptoms", "Confidence", "Source", "Match"])
    if show_farmer:
        columns.append("Type")
    return pd.DataFrame(rows)[columns]


def render_consultation_history_page(
    farmer_id: int | None = None,
    allow_farmer_filter: bool = False,
    page_title: str = "My History",
) -> None:
    render_page_header(
        page_title,
        "View past consultations, inspect submitted symptoms, and prepare PDF reports."
        if allow_farmer_filter
        else "Review your diagnoses and prepare editable PDF reports.",
    )

    service = ConsultationService()
    selected_farmer_id = farmer_id
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

    show_farmer = False
    if allow_farmer_filter:
        with col2:
            farmers = get_all_farmers()
            options: dict[str, int | None] = {"All farmers": None}
            options.update({f["full_name"]: f["id"] for f in farmers})
            choice = st.selectbox("Farmer", list(options), index=0)
            selected_farmer_id = options[choice]
            show_farmer = selected_farmer_id is None

    history = service.get_history(
        farmer_id=selected_farmer_id,
        diagnosis_source=diagnosis_source,
    )
    if not history:
        st.info("No consultations found for this filter.")
        return

    df = _history_dataframe(history, show_farmer=show_farmer)
    event = st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "ID": st.column_config.NumberColumn("ID", format="%d", width="small"),
            "Symptoms": st.column_config.TextColumn("Submitted symptoms", width="large"),
            "Confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0, max_value=100, format="%d%%"
            ),
        },
    )

    selected_rows = event.selection.rows if event and event.selection else []
    if not selected_rows:
        st.caption("Select a consultation to inspect its details and prepare a report.")
        return

    cid = int(df.iloc[selected_rows[0]]["ID"])
    details_tab, export_tab = st.tabs(["Consultation details", "Edit and export PDF"])
    with details_tab:
        render_history_detail(cid)
    with export_tab:
        render_pdf_export_editor(cid)