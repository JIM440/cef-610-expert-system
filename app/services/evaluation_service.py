"""Honest Phase 9 evaluation for stored hybrid consultations."""

from app.database import fetch_one


def get_hybrid_evaluation() -> dict:
    row = fetch_one(
        """
        SELECT COUNT(*) AS eligible_consultations,
               COUNT(*) FILTER (WHERE final_disease_id=ai_predicted_disease_id) AS agreements
        FROM consultation
        WHERE final_disease_id IS NOT NULL
          AND ai_predicted_disease_id IS NOT NULL
        """
    ) or {"eligible_consultations": 0, "agreements": 0}
    eligible = int(row["eligible_consultations"] or 0)
    agreements = int(row["agreements"] or 0)
    return {
        "eligible_consultations": eligible,
        "agreements": agreements,
        "disagreements": eligible - agreements,
        "agreement_rate": round((agreements / eligible) * 100, 1) if eligible else None,
        "evaluation_basis": (
            "Agreement between the rule-based result and knowledge-base-derived "
            "Naive Bayes prediction on stored consultations containing both results."
        ),
        "held_out_dataset": False,
        "limitation": (
            "This is not accuracy, precision, recall, or held-out test performance. "
            "No independent ground-truth dataset is currently available."
        ),
    }
