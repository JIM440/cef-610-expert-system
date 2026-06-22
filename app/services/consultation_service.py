from app.repositories import consultation_repository as repo
from app.services.pdf_service import PdfService


class ConsultationService:
    def __init__(self) -> None:
        self.pdf = PdfService()

    def get_history(
        self,
        farmer_id: int | None = None,
        diagnosis_source: str = "all",
        limit: int = 50,
    ) -> list[dict]:
        return repo.get_consultation_history(
            farmer_id=farmer_id,
            diagnosis_source=diagnosis_source,
            limit=limit,
        )

    def get_image_analysis(self, consultation_id: int) -> dict | None:
        return repo.get_consultation_image(consultation_id)

    def get_detail(self, consultation_id: int) -> list[dict]:
        return repo.get_diagnosis_detail(consultation_id)

    def get_summary(self, consultation_id: int) -> dict | None:
        return repo.get_consultation_summary(consultation_id)

    def get_latest_report(self, consultation_id: int) -> dict | None:
        summary = repo.get_consultation_summary(consultation_id)
        if not summary:
            return None
        return {
            "report_title": f"Consultation Report #{consultation_id}",
            "summary": summary.get("explanation") or "",
            "notes": "",
            "recommendations": summary.get("treatments") or "",
        }

    def export_pdf(
        self,
        consultation_id: int,
        report_title: str,
        summary: str,
        notes: str,
        recommendations: str,
    ) -> bytes:
        return self.pdf.build_consultation_pdf(
            consultation_id, report_title, summary, notes, recommendations
        )
