from app.expert_system.rule_matcher import RuleMatchResult


def calculate_confidence(matches: list[RuleMatchResult]) -> int:
    if not matches:
        return 0
    return max(match.matched_score for match in matches)


def pick_best_match(matches: list[RuleMatchResult]) -> RuleMatchResult | None:
    if not matches:
        return None
    return max(matches, key=lambda m: m.matched_score)
