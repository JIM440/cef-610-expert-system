"""
Inference engine - uses Rule Knowledge only (rule_symptom, rule_environment).

Does NOT read disease_symptom. Disease facts are for display and context,
not for rule matching. See README.md.
"""

from dataclasses import dataclass

from app.expert_system.confidence_calculator import calculate_confidence, pick_best_match
from app.expert_system.explanation_builder import (
    build_explanation,
    build_reason_lines,
    build_result_title,
)
from app.expert_system.rule_matcher import (
    RuleMatchResult,
    build_rule_definitions,
    match_rules,
)
from app.repositories.rule_repository import get_active_rules_for_crop


@dataclass
class DiagnosisOutput:
    disease_id: int
    disease_name: str
    result_title: str
    explanation: str
    confidence: int
    matches: list[RuleMatchResult]
    best_match: RuleMatchResult
    reason_lines: dict
    match_tier: str


class InferenceEngine:
    def diagnose(
        self,
        crop_id: int,
        symptom_ids: list[int],
        condition_value_ids: list[int],
    ) -> DiagnosisOutput | None:
        rows = get_active_rules_for_crop(crop_id)
        rules = build_rule_definitions(rows)
        matches = match_rules(
            rules,
            set(symptom_ids),
            set(condition_value_ids),
            allow_partial=True,
            low_threshold=0.5,
        )

        if not matches:
            return None

        best = pick_best_match(matches)
        assert best is not None

        symptom_names = {}
        condition_labels = {}
        for rule in rules.values():
            symptom_names.update(rule.symptom_names)
            condition_labels.update(rule.condition_labels)

        title = build_result_title(best.disease_name)
        explanation = build_explanation(best)
        if best.match_tier == "LOW":
            title = f"Low confidence possible match: {best.disease_name}"
            explanation = (
                "This is a low-confidence possible match because only part of the expert rule matched. "
                + explanation
            )

        return DiagnosisOutput(
            disease_id=best.disease_id,
            disease_name=best.disease_name,
            result_title=title,
            explanation=explanation,
            confidence=calculate_confidence(matches),
            matches=matches,
            best_match=best,
            reason_lines=build_reason_lines(best, symptom_names, condition_labels),
            match_tier=best.match_tier,
        )
