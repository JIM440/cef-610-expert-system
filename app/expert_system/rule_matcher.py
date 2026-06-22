from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class RuleDefinition:
    rule_id: int
    rule_name: str
    disease_id: int
    disease_name: str
    confidence_score: int
    explanation_template: str
    required_symptoms: set[int] = field(default_factory=set)
    required_conditions: set[int] = field(default_factory=set)
    symptom_names: dict[int, str] = field(default_factory=dict)
    condition_labels: dict[int, str] = field(default_factory=dict)


@dataclass
class RuleMatchResult:
    rule_id: int
    rule_name: str
    disease_id: int
    disease_name: str
    confidence_score: int
    matched_score: int
    explanation_template: str
    matched_symptom_ids: list[int]
    matched_condition_ids: list[int]
    missing_symptom_ids: list[int]
    missing_condition_ids: list[int]
    match_tier: str = "HIGH"


def build_rule_definitions(rows: list[dict]) -> dict[int, RuleDefinition]:
    rules: dict[int, RuleDefinition] = {}
    for row in rows:
        rule_id = row["rule_id"]
        if rule_id not in rules:
            rules[rule_id] = RuleDefinition(
                rule_id=rule_id,
                rule_name=row["rule_name"],
                disease_id=row["disease_id"],
                disease_name=row["disease_name"],
                confidence_score=row["confidence_score"],
                explanation_template=row["explanation_template"] or "",
            )
        rule = rules[rule_id]
        if row["symptom_id"] and row.get("symptom_required", True):
            rule.required_symptoms.add(row["symptom_id"])
            rule.symptom_names[row["symptom_id"]] = row["symptom_name"]
        factor_id = row.get("environmental_factor_id") or row.get("condition_value_id")
        if factor_id and row.get("condition_required", True):
            rule.required_conditions.add(factor_id)
            label = f"{row['condition_name']}: {row['condition_value']}"
            rule.condition_labels[factor_id] = label
    return rules


def _score_rule(
    rule: RuleDefinition,
    symptom_ids: set[int],
    condition_value_ids: set[int],
    allow_partial: bool,
    low_threshold: float,
) -> RuleMatchResult | None:
    matched_symptoms = rule.required_symptoms & symptom_ids
    matched_conditions = rule.required_conditions & condition_value_ids
    missing_symptoms = rule.required_symptoms - symptom_ids
    missing_conditions = rule.required_conditions - condition_value_ids

    total_required = len(rule.required_symptoms) + len(rule.required_conditions)
    if total_required == 0:
        return None

    matched_count = len(matched_symptoms) + len(matched_conditions)
    ratio = matched_count / total_required
    if matched_count == total_required:
        tier = "HIGH"
    elif allow_partial and ratio >= low_threshold:
        tier = "LOW"
    else:
        return None

    matched_score = int(ratio * rule.confidence_score)
    return RuleMatchResult(
        rule_id=rule.rule_id,
        rule_name=rule.rule_name,
        disease_id=rule.disease_id,
        disease_name=rule.disease_name,
        confidence_score=rule.confidence_score,
        matched_score=matched_score,
        explanation_template=rule.explanation_template,
        matched_symptom_ids=sorted(matched_symptoms),
        matched_condition_ids=sorted(matched_conditions),
        missing_symptom_ids=sorted(missing_symptoms),
        missing_condition_ids=sorted(missing_conditions),
        match_tier=tier,
    )


def match_rules(
    rules: dict[int, RuleDefinition],
    symptom_ids: set[int],
    condition_value_ids: set[int],
    allow_partial: bool = False,
    low_threshold: float = 0.5,
) -> list[RuleMatchResult]:
    results: list[RuleMatchResult] = []

    for rule in rules.values():
        result = _score_rule(rule, symptom_ids, condition_value_ids, allow_partial, low_threshold)
        if result:
            results.append(result)

    if not results and allow_partial:
        fallback_results: list[RuleMatchResult] = []
        for rule in rules.values():
            result = _score_rule(
                rule,
                symptom_ids,
                condition_value_ids,
                allow_partial=True,
                low_threshold=0.0,
            )
            if result and (result.matched_symptom_ids or result.matched_condition_ids):
                result.match_tier = "LOW"
                fallback_results.append(result)
        if fallback_results:
            best_score = max(result.matched_score for result in fallback_results)
            results = [
                result
                for result in fallback_results
                if result.matched_score == best_score
            ]

    results.sort(key=lambda r: (r.match_tier == "HIGH", r.matched_score), reverse=True)
    return results


def group_matches_by_disease(matches: list[RuleMatchResult]) -> dict[int, list[RuleMatchResult]]:
    grouped: dict[int, list[RuleMatchResult]] = defaultdict(list)
    for match in matches:
        grouped[match.disease_id].append(match)
    return dict(grouped)
