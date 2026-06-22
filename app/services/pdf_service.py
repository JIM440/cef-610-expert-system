from io import BytesIO

from fpdf import FPDF

from app.repositories.consultation_repository import get_consultation_summary


def _pdf_text(value: object) -> str:
    return str(value or "").encode("latin-1", "replace").decode("latin-1")


class PdfService:
    def build_consultation_pdf(
        self,
        consultation_id: int,
        report_title: str,
        summary: str,
        notes: str,
        recommendations: str,
    ) -> bytes:
        row = get_consultation_summary(consultation_id)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(0, 9, _pdf_text(report_title))
        pdf.ln(2)

        if row:
            pdf.set_font("Helvetica", size=10)
            fields = [
                ("Farmer", row.get("farmer_name") or "General consultation"),
                ("Performed by", row.get("performed_by_name") or row.get("performed_by")),
                ("Crop", row.get("crop_name")),
                ("Disease", row.get("disease_name")),
                ("Confidence", f"{row.get('confidence_score') or 0}%"),
                ("Date", row.get("consultation_date")),
                ("Source", "Image recognition" if row.get("source") == "IMAGE" else "Manual symptom selection"),
            ]
            for label, value in fields:
                pdf.cell(0, 6, _pdf_text(f"{label}: {value or '-'}"), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            self._section(pdf, "Submitted Symptoms", row.get("symptoms") or "-")

        self._section(pdf, "Summary", summary)
        self._section(pdf, "Diagnosis Explanation", row.get("explanation") if row else "")
        self._section(pdf, "Recommended Treatments", row.get("treatments") if row else "")
        self._section(pdf, "Expert Notes", notes)
        self._section(pdf, "Recommendations", recommendations)

        buffer = BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()

    @staticmethod
    def _section(pdf: FPDF, heading: str, body: object) -> None:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 7, _pdf_text(heading), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(0, 6, _pdf_text(body))
        pdf.ln(2)