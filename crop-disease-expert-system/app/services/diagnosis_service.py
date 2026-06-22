from app.expert_system.ai_predictor import NaiveBayesPredictor
from app.expert_system.inference_engine import InferenceEngine
from app.repositories import consultation_repository as consult_repo
from app.repositories import disease_repository as disease_repo
from app.repositories import rule_repository as rule_repo
from app.utils.consultation_types import (
    ADMIN_FOR_FARMER,
    ADMIN_GENERAL,
    FARMER_SELF,
)


class DiagnosisService:
    def __init__(self) -> None:
        self.engine = InferenceEngine()
        self.ai_predictor = NaiveBayesPredictor()

    def run_diagnosis(
        self,
        crop_id: int,
        symptom_ids: list[int],
        condition_value_ids: list[int],
        performed_by_user_id: int,
        consultation_type: str,
        farmer_id: int | None = None,
        source: str = "SYMPTOMS",
        gemini_raw_extraction: str | None = None,
    ) -> dict | None:
        rule_result = self.engine.diagnose(crop_id, symptom_ids, condition_value_ids)
        ai_result = self.ai_predictor.predict(
            symptom_ids,
            condition_value_ids,
            crop_id=crop_id,
        )
        if not rule_result and not ai_result:
            return None

        consultation_id = consult_repo.create_consultation(
            performed_by_user_id=performed_by_user_id,
            consultation_type=consultation_type,
            farmer_id=farmer_id,
            crop_id=crop_id,
            disease_id=rule_result.disease_id if rule_result else None,
            confidence=rule_result.confidence if rule_result else None,
            source=source,
            match_tier=rule_result.match_tier if rule_result else "NONE",
            gemini_raw_extraction=gemini_raw_extraction,
            matched_rule_id=rule_result.best_match.rule_id if rule_result else None,
            explanation=rule_result.explanation if rule_result else "No expert rule matched the submitted evidence.",
            ai_predicted_disease_id=ai_result.disease_id if ai_result else None,
            ai_confidence=ai_result.confidence if ai_result else None,
            ai_model_version=ai_result.model_version if ai_result else None,
        )

        matched_symptoms = set(rule_result.best_match.matched_symptom_ids) if rule_result else set()
        matched_conditions = set(rule_result.best_match.matched_condition_ids) if rule_result else set()
        for sid in symptom_ids:
            consult_repo.add_consultation_symptom(
                consultation_id,
                sid,
                matched=sid in matched_symptoms,
            )
        for cid in condition_value_ids:
            consult_repo.add_consultation_environment(
                consultation_id,
                cid,
                matched=cid in matched_conditions,
            )

        treatments: list[dict] = []
        if rule_result:
            treatments = rule_repo.get_treatments_for_rule(rule_result.best_match.rule_id)
            if not treatments:
                treatments = disease_repo.get_treatments_for_disease(rule_result.disease_id)
            for treatment in treatments:
                consult_repo.add_consultation_treatment(consultation_id, treatment["id"])

        agreement = bool(
            rule_result
            and ai_result
            and rule_result.disease_id == ai_result.disease_id
        )
        return {
            "consultation_id": consultation_id,
            "consultation_type": consultation_type,
            "diagnosis_result_id": consultation_id,
            "disease_id": rule_result.disease_id if rule_result else None,
            "disease_name": rule_result.disease_name if rule_result else None,
            "result_title": rule_result.result_title if rule_result else "No rule-based diagnosis",
            "explanation": rule_result.explanation if rule_result else "No expert rule matched the submitted evidence.",
            "confidence": rule_result.confidence if rule_result else 0,
            "reasons": rule_result.reason_lines if rule_result else {},
            "treatments": treatments,
            "matched_rule_id": rule_result.best_match.rule_id if rule_result else None,
            "match_tier": rule_result.match_tier if rule_result else "NONE",
            "ai_prediction": {
                "disease_id": ai_result.disease_id,
                "disease_name": ai_result.disease_name,
                "confidence": ai_result.confidence,
                "model_version": ai_result.model_version,
            } if ai_result else None,
            "methods_agree": agreement if rule_result and ai_result else None,
        }

    @staticmethod
    def resolve_consultation_type(
        is_admin: bool,
        farmer_id: int | None,
        actor_farmer_id: int | None,
    ) -> tuple[str, int | None]:
        if not is_admin:
            return FARMER_SELF, actor_farmer_id
        if farmer_id is not None:
            return ADMIN_FOR_FARMER, farmer_id
        return ADMIN_GENERAL, None
