from app.expert_system.rule_matcher import RuleDefinition, match_rules


def test_partial_matching_returns_best_overlap_below_threshold():
    weak = RuleDefinition(
        rule_id=1,
        rule_name="Weak overlap",
        disease_id=10,
        disease_name="Early Blight",
        confidence_score=80,
        explanation_template="",
        required_symptoms={1, 2, 3, 4},
    )
    stronger = RuleDefinition(
        rule_id=2,
        rule_name="Stronger overlap",
        disease_id=20,
        disease_name="Late Blight",
        confidence_score=90,
        explanation_template="",
        required_symptoms={1, 2, 3},
    )

    matches = match_rules(
        {1: weak, 2: stronger},
        symptom_ids={1},
        condition_value_ids=set(),
        allow_partial=True,
        low_threshold=0.5,
    )

    assert len(matches) == 1
    assert matches[0].rule_id == 2
    assert matches[0].match_tier == "LOW"


def test_partial_matching_requires_at_least_one_overlap():
    rule = RuleDefinition(
        rule_id=1,
        rule_name="No overlap",
        disease_id=10,
        disease_name="Early Blight",
        confidence_score=80,
        explanation_template="",
        required_symptoms={2, 3},
    )

    matches = match_rules(
        {1: rule},
        symptom_ids={1},
        condition_value_ids=set(),
        allow_partial=True,
    )

    assert matches == []
