from app.services.pdf_service import PdfService


def test_bulk_history_pdf_is_generated_from_multiline_content():
    content = "CONSULTATION 1\n" + "=" * 72 + "\nRule-Based Result: Early Blight\nAI Prediction: Early Blight"
    pdf = PdfService().build_history_pdf("Consultation History", content)
    assert pdf.startswith(b"%PDF")
    assert len(pdf) > 500
