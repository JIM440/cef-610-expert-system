from app.expert_system.confidence_calculator import calculate_confidence, pick_best_match
from app.expert_system.rule_matcher import RuleMatchResult


def test_pick_best_match_returns_highest_scoring_rule():
    matches = [
        RuleMatchResult(1, "R1", 1, "A", 80, 70, "", [], [], [], []),
        RuleMatchResult(2, "R2", 2, "B", 90, 90, "", [], [], [], []),
    ]
    best = pick_best_match(matches)
    assert best is not None
    assert best.disease_name == "B"
    assert calculate_confidence(matches) == 90
