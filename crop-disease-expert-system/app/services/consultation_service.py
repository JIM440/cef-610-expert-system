from app.repositories import consultation_repository as repo
from app.services.pdf_service import PdfService


class ConsultationService:
    def __init__(self) -> None:
        self.pdf = PdfService()

    def get_history(
        self,
        farmer_id: int | None = None,
        diagnosis_source: str = "all",
        limit: int | None = None,
    ) -> list[dict]:
        return repo.get_consultation_history(
            farmer_id=farmer_id,
            diagnosis_source=diagnosis_source,
            limit=limit,
        )

    def export_history_pdf(self, report_title: str, report_content: str) -> bytes:
        return self.pdf.build_history_pdf(report_title, report_content)
