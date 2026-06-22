from app.config import GEMINI_CONFIG
from app.ai.image_analyzer import analyze_image_bytes
from app.database import execute
from app.repositories.crop_repository import get_tomato_crop_id
from app.services.diagnosis_service import DiagnosisService
from app.utils.consultation_types import (
    IMAGE_ADMIN_FOR_FARMER,
    IMAGE_ADMIN_GENERAL,
    IMAGE_FARMER_SELF,
)


class ImageRecognitionService:
    def __init__(self) -> None:
        self.diagnosis = DiagnosisService()

    def analyze_and_diagnose(
        self,
        image_bytes: bytes,
        original_filename: str,
        performed_by_user_id: int,
        consultation_type: str,
        farmer_id: int | None,
        crop_id: int | None = None,
        condition_value_ids: list[int] | None = None,
    ) -> dict | None:
        analysis = analyze_image_bytes(image_bytes, original_filename)
        symptom_ids = analysis["symptom_ids"]
        if not symptom_ids:
            return {"analysis": analysis, "diagnosis": None}

        if crop_id is None:
            crop_id = get_tomato_crop_id()
        if crop_id is None:
            return None

        raw_extraction = self._format_raw_extraction(analysis)
        result = self.diagnosis.run_diagnosis(
            crop_id=crop_id,
            symptom_ids=symptom_ids,
            condition_value_ids=condition_value_ids or [],
            performed_by_user_id=performed_by_user_id,
            consultation_type=consultation_type,
            farmer_id=farmer_id,
            source="IMAGE",
            gemini_raw_extraction=raw_extraction,
        )
        if not result:
            return {"analysis": analysis, "diagnosis": None}

        self._save_analysis_record(
            result["consultation_id"],
            original_filename,
            analysis["analysis_summary"],
            analysis.get("visual_summary", ""),
            analysis.get("analysis_source", "gemini"),
            GEMINI_CONFIG.model,
        )
        return {
            "analysis": analysis,
            "diagnosis": result,
        }

    @staticmethod
    def resolve_image_consultation_type(
        is_admin: bool,
        farmer_id: int | None,
        actor_farmer_id: int | None,
    ) -> tuple[str, int | None]:
        if not is_admin:
            return IMAGE_FARMER_SELF, actor_farmer_id
        if farmer_id is not None:
            return IMAGE_ADMIN_FOR_FARMER, farmer_id
        return IMAGE_ADMIN_GENERAL, None

    @staticmethod
    def _format_raw_extraction(analysis: dict) -> str:
        lines = []
        if analysis.get("visual_summary"):
            lines.append(f"Visual summary: {analysis['visual_summary']}")
        detected = analysis.get("detected_symptoms") or []
        if detected:
            lines.append("Detected symptoms:")
            lines.extend(
                f"- {item['symptom_name']} ({item['score']}%)" for item in detected
            )
        return "\n".join(lines) or analysis.get("analysis_summary", "")

    def _save_analysis_record(
        self,
        consultation_id: int,
        original_filename: str,
        analysis_summary: str,
        visual_summary: str,
        analysis_source: str,
        gemini_model: str,
    ) -> None:
        execute(
            """
            INSERT INTO consultation_image (
                consultation_id, original_filename, analysis_summary,
                visual_summary, analysis_source, gemini_model
            )
            VALUES (
                %(cid)s, %(name)s, %(summary)s,
                %(visual)s, %(source)s, %(model)s
            )
            """,
            {
                "cid": consultation_id,
                "name": original_filename,
                "summary": analysis_summary,
                "visual": visual_summary or None,
                "source": analysis_source,
                "model": gemini_model,
            },
        )
