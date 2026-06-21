from io import BytesIO

from fpdf import FPDF

from app.repositories.consultation_repository import get_consultation_summary


class PdfService:
    def build_consultation_pdf(
        self,
        consultation_id: int,
        report_title: str,
        summary: str,
        notes: str,
        recommendations: str,
    ) -> bytes:
        summary_row = get_consultation_summary(consultation_id)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, report_title, ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.ln(4)

        if summary_row:
            pdf.cell(0, 8, f"Farmer: {summary_row.get('farmer_name') or 'N/A'}", ln=True)
            pdf.cell(0, 8, f"Crop: {summary_row.get('crop_name', '')}", ln=True)
            pdf.cell(0, 8, f"Disease: {summary_row.get('disease_name', '')}", ln=True)
            pdf.cell(0, 8, f"Confidence: {summary_row.get('confidence_score', '')}%", ln=True)
            pdf.cell(0, 8, f"Date: {summary_row.get('consultation_date', '')}", ln=True)
            pdf.ln(4)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Summary", ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, summary or "")
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Diagnosis Explanation", ln=True)
        pdf.set_font("Helvetica", size=11)
        explanation = summary_row.get("explanation", "") if summary_row else ""
        pdf.multi_cell(0, 6, explanation or "")
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Notes", ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, notes or "")
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Recommendations", ln=True)
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, recommendations or "")

        buffer = BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()
