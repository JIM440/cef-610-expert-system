from app.expert_system.rule_matcher import RuleDefinition, match_rules


def test_rule_matches_when_all_symptoms_and_conditions_present():
    rule = RuleDefinition(
        rule_id=1,
        rule_name="Test Rule",
        disease_id=10,
        disease_name="Early Blight",
        confidence_score=85,
        explanation_template="Test explanation",
        required_symptoms={1, 2},
        required_conditions={5},
        symptom_names={1: "Brown spots", 2: "Yellowing"},
        condition_labels={5: "Humidity: High"},
    )
    matches = match_rules({1: rule}, symptom_ids={1, 2}, condition_value_ids={5})
    assert len(matches) == 1
    assert matches[0].disease_name == "Early Blight"
    assert matches[0].matched_score == 85


def test_rule_does_not_match_when_symptom_missing():
    rule = RuleDefinition(
        rule_id=1,
        rule_name="Test Rule",
        disease_id=10,
        disease_name="Early Blight",
        confidence_score=85,
        explanation_template="",
        required_symptoms={1, 2},
        required_conditions=set(),
    )
    matches = match_rules({1: rule}, symptom_ids={1}, condition_value_ids=set())
    assert matches == []
