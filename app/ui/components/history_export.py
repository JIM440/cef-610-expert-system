import streamlit as st

from app.services.consultation_service import ConsultationService
from app.utils.consultation_types import is_image_consultation


def render_history_detail(consultation_id: int) -> None:
    service = ConsultationService()
    summary = service.get_summary(consultation_id)
    detail = service.get_detail(consultation_id)
    if not summary or not detail:
        st.warning("No diagnosis detail found.")
        return

    row = detail[0]
    if is_image_consultation(row.get("consultation_type")):
        image_row = service.get_image_analysis(consultation_id)
        if image_row:
            with st.container(border=True):
                st.markdown("**Gemini image analysis**")
                st.write(image_row.get("visual_summary") or "No visual summary returned.")
                if image_row.get("analysis_summary"):
                    st.caption(image_row["analysis_summary"])

    st.subheader(row["result_title"])
    st.write(row["explanation"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Confidence", f"{row['confidence_score']}%")
    c2.metric("Symptoms", len([x for x in (summary.get("symptoms") or "").split(", ") if x and x != "-"]))
    c3.metric("Source", "Image" if summary.get("source") == "IMAGE" else "Manual")

    with st.container(border=True):
        st.markdown("**Submitted symptoms**")
        st.write(summary.get("symptoms") or "-")

    seen: set[tuple] = set()
    with st.container(border=True):
        st.markdown("**Rule evidence**")
        for item in detail:
            values = (
                item.get("reason_symptom_name"),
                item.get("reason_condition_name"),
                item.get("reason_condition_value"),
                item.get("rule_name"),
            )
            if values in seen:
                continue
            seen.add(values)
            if values[0]:
                st.write(f"- Symptom: {values[0]}")
            if values[1]:
                st.write(f"- Condition: {values[1]} = {values[2]}")
            if values[3]:
                st.write(f"- Rule: {values[3]} ({item.get('matched_score', 0)}%)")

    with st.container(border=True):
        st.markdown("**Recommended treatments**")
        st.write(summary.get("treatments") or "No treatments recorded.")


def render_pdf_export_editor(consultation_id: int) -> None:
    service = ConsultationService()
    summary_row = service.get_summary(consultation_id)
    if not summary_row:
        st.warning("Consultation summary is unavailable.")
        return

    saved = service.get_latest_report(consultation_id) or {}
    disease = summary_row.get("disease_name") or "Consultation"
    default_summary = (
        f"Diagnosis: {disease}. Submitted symptoms: {summary_row.get('symptoms') or '-'}"
    )
    default_recommendations = summary_row.get("treatments") or "Follow the expert treatment plan and monitor the crop."

    st.markdown("**Prepare report content**")
    st.caption("Review and edit every field below before generating the PDF.")
    with st.form(f"pdf_editor_{consultation_id}"):
        report_title = st.text_input(
            "Report title",
            value=saved.get("report_title") or f"Tomato diagnosis report: {disease}",
        )
        summary = st.text_area(
            "Summary",
            value=saved.get("summary") or default_summary,
            height=120,
        )
        notes = st.text_area(
            "Expert notes",
            value=saved.get("notes") or "",
            height=120,
        )
        recommendations = st.text_area(
            "Recommendations",
            value=saved.get("recommendations") or default_recommendations,
            height=140,
        )
        generate = st.form_submit_button("Generate PDF", type="primary", width="stretch")

    state_key = f"pdf_bytes_{consultation_id}"
    if generate:
        try:
            st.session_state[state_key] = service.export_pdf(
                consultation_id,
                report_title.strip() or "Consultation report",
                summary,
                notes,
                recommendations,
            )
            st.success("PDF generated from the edited content.")
        except Exception as exc:
            st.error(f"Could not generate PDF: {exc}")

    pdf_bytes = st.session_state.get(state_key)
    if pdf_bytes:
        st.download_button(
            "Download PDF report",
            data=pdf_bytes,
            file_name=f"consultation_{consultation_id}.pdf",
            mime="application/pdf",
            width="stretch",
        )