from app.expert_system.rule_matcher import RuleMatchResult


def build_result_title(disease_name: str) -> str:
    return f"Possible disease: {disease_name}"


def build_explanation(best: RuleMatchResult) -> str:
    if best.explanation_template:
        return best.explanation_template
    return (
        f"The crop is likely affected by {best.disease_name} "
        f"because observed symptoms and conditions match expert rule {best.rule_name}."
    )


def build_reason_lines(
    best: RuleMatchResult,
    symptom_names: dict[int, str],
    condition_labels: dict[int, str],
) -> dict:
    return {
        "symptoms": [symptom_names[sid] for sid in best.matched_symptom_ids if sid in symptom_names],
        "conditions": [
            condition_labels[cid] for cid in best.matched_condition_ids if cid in condition_labels
        ],
        "rule": {
            "rule_id": best.rule_id,
            "rule_name": best.rule_name,
            "matched_score": best.matched_score,
        },
    }
