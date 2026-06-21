from app.expert_system.inference_engine import InferenceEngine
from app.repositories import consultation_repository as consult_repo
from app.repositories import diagnosis_repository as diag_repo
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
        result = self.engine.diagnose(crop_id, symptom_ids, condition_value_ids)
        if not result:
            return None

        consultation_id = consult_repo.create_consultation(
            performed_by_user_id=performed_by_user_id,
            consultation_type=consultation_type,
            farmer_id=farmer_id,
            crop_id=crop_id,
            disease_id=result.disease_id,
            confidence=result.confidence,
            source=source,
            match_tier=result.match_tier,
            gemini_raw_extraction=gemini_raw_extraction,
        )

        matched_symptoms = set(result.best_match.matched_symptom_ids)
        matched_conditions = set(result.best_match.matched_condition_ids)
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

        treatments = rule_repo.get_treatments_for_rule(result.best_match.rule_id)
        if not treatments:
            treatments = disease_repo.get_treatments_for_disease(result.disease_id)
        for t in treatments:
            consult_repo.add_consultation_treatment(consultation_id, t["id"])

        result_id = diag_repo.save_diagnosis_result(
            consultation_id,
            result.disease_id,
            result.result_title,
            result.explanation,
            result.confidence,
        )

        symptom_type_id = diag_repo.get_reason_type_id("symptom_match")
        env_type_id = diag_repo.get_reason_type_id("environment_match")
        rule_type_id = diag_repo.get_reason_type_id("rule_match")

        order = 0
        if symptom_type_id and result.reason_lines["symptoms"]:
            reason_id = diag_repo.save_diagnosis_reason(
                result_id, symptom_type_id, None, order
            )
            for sid in result.best_match.matched_symptom_ids:
                diag_repo.link_reason_symptom(reason_id, sid)
            order += 1

        if env_type_id and result.reason_lines["conditions"]:
            reason_id = diag_repo.save_diagnosis_reason(
                result_id, env_type_id, None, order
            )
            for cid in result.best_match.matched_condition_ids:
                diag_repo.link_reason_environment(reason_id, cid)
            order += 1

        if rule_type_id:
            diag_repo.save_diagnosis_reason(
                result_id,
                rule_type_id,
                result.best_match.rule_id,
                order,
            )
            diag_repo.save_rule_match(
                result_id, result.best_match.rule_id, result.best_match.matched_score
            )

        return {
            "consultation_id": consultation_id,
            "consultation_type": consultation_type,
            "diagnosis_result_id": result_id,
            "disease_id": result.disease_id,
            "disease_name": result.disease_name,
            "result_title": result.result_title,
            "explanation": result.explanation,
            "confidence": result.confidence,
            "reasons": result.reason_lines,
            "treatments": treatments,
            "matched_rule_id": result.best_match.rule_id,
            "match_tier": result.match_tier,
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
