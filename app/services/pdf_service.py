from io import BytesIO

from fpdf import FPDF


def _pdf_text(value: object) -> str:
    return str(value or "").encode("latin-1", "replace").decode("latin-1")


class PdfService:
    def build_history_pdf(self, report_title: str, report_content: str) -> bytes:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(
            0, 9, _pdf_text(report_title),
            new_x="LMARGIN", new_y="NEXT",
        )
        pdf.ln(2)
        pdf.set_font("Helvetica", size=9)
        for line in report_content.splitlines():
            pdf.multi_cell(
                0, 5, _pdf_text(line) if line else " ",
                new_x="LMARGIN", new_y="NEXT",
            )

        buffer = BytesIO()
        pdf.output(buffer)
        return buffer.getvalue()
