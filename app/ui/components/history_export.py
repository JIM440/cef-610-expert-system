import streamlit as st

from app.services.consultation_service import ConsultationService
from app.utils.consultation_types import is_image_consultation


def render_history_detail(consultation_id: int) -> None:
    service = ConsultationService()
    detail = service.get_detail(consultation_id)
    if not detail:
        st.warning("No diagnosis detail found.")
        return

    row = detail[0]
    if is_image_consultation(row.get("consultation_type")):
        image_row = service.get_image_analysis(consultation_id)
        if image_row:
            st.markdown("**Gemini image analysis**")
            if image_row.get("visual_summary"):
                st.write(image_row["visual_summary"])
            if image_row.get("analysis_summary"):
                st.caption(image_row["analysis_summary"])

    st.subheader(row["result_title"])
    st.write(row["explanation"])
    st.metric("Confidence", f"{row['confidence_score']}%")

    for item in detail:
        if item.get("reason_symptom_name"):
            st.write(f"- Symptom: {item['reason_symptom_name']}")
        if item.get("reason_condition_name"):
            st.write(
                f"- Condition: {item['reason_condition_name']} = "
                f"{item['reason_condition_value']}"
            )
        if item.get("rule_name"):
            st.write(f"- Rule: {item['rule_name']} ({item['matched_score']}%)")


def render_pdf_export_modal(consultation_id: int, default_title: str) -> None:
    with st.expander("Export PDF report", expanded=False):
        report_title = st.text_input("Title", value=default_title)
        summary = st.text_area("Summary", value="Consultation diagnosis summary.")
        notes = st.text_area("Notes", value="")
        recommendations = st.text_area(
            "Recommendations",
            value="Follow the suggested treatments and monitor the crop.",
        )
        if st.button("Generate PDF"):
            service = ConsultationService()
            pdf_bytes = service.export_pdf(
                consultation_id, report_title, summary, notes, recommendations
            )
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=f"consultation_{consultation_id}.pdf",
                mime="application/pdf",
            )
