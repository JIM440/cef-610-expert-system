from app.expert_system.explanation_builder import build_explanation, build_result_title
from app.expert_system.rule_matcher import RuleMatchResult


def test_build_result_title():
    assert build_result_title("Early Blight") == "Possible disease: Early Blight"


def test_build_explanation_uses_template():
    match = RuleMatchResult(
        rule_id=1,
        rule_name="EB-Rule-01",
        disease_id=1,
        disease_name="Early Blight",
        confidence_score=85,
        matched_score=85,
        explanation_template="Template text here.",
        matched_symptom_ids=[],
        matched_condition_ids=[],
        missing_symptom_ids=[],
        missing_condition_ids=[],
    )
    assert build_explanation(match) == "Template text here."
