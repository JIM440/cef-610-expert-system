# System Architecture

## Diagnosis pipeline

```text
Manual selection or tomato image
             |
             v
Database symptom and environmental-factor IDs
             |
             v
RuleMatcher evaluates active PostgreSQL rules
             |
             v
InferenceEngine selects the best rule
             |
             v
Consultation stores disease, confidence, rule, explanation, evidence, and treatments
             |
             v
History dashboard and on-demand PDF report
```

For image recognition, Gemini returns visible symptom names and a visual summary. The application maps those names to the existing `symptom` rows before invoking the same rule engine used by manual diagnosis.

## Application layers

| Layer | Responsibility |
|---|---|
| `app/ui` | Streamlit navigation, forms, cards, history, and PDF export workflow |
| `app/services` | Diagnosis, image-recognition, consultation, and reporting workflows |
| `app/expert_system` | Rule grouping, scoring, fallback matching, and inference |
| `app/repositories` | SQL access to the consolidated schema |
| `app/ai` | Gemini connection and structured symptom extraction |
| `database` | Canonical schema, current seed data, and one-time consolidation SQL |

## Knowledge model

`disease_symptom` stores descriptive disease knowledge for disease views. Diagnostic decisions use `rule`, `rule_symptom`, `rule_environment`, and `rule_treatment`.

Environmental choices are normalized as rows in `environmental_factor`, each containing a category, value name, and optional unit.

## Consultation model

`consultation` is one diagnosis event. It stores the actor, optional farmer, crop, source, final disease, confidence, matched rule, explanation, and Gemini extraction text. Its three junction tables record the selected/matched symptoms, environmental factors, and recommended treatments.

PDF reports are assembled from these tables when requested. No report record or uploaded image record is persisted.

## Authentication

All users are stored in `app_user`. `role` is constrained to `ADMIN`, `EXPERT`, or `FARMER`; authentication and sidebar access are database-driven.