# Final System Design (Locked)

## Removed from scope

The following pages are **not** part of the final system:

- Settings
- About
- AI Model Management

They are not required by the project brief and add complexity without contributing to assessment objectives.

---

## Design changes from initial concept

| Change | Final approach |
|--------|----------------|
| No hardcoded rules | `rule`, `rule_symptom`, `rule_environment`, `rule_treatment` via FKs |
| No arrays/JSON | One relationship per row in junction tables |
| Farmer role | Admin + Farmer with `role`, `app_user`, `farmer` profile |
| Diagnosis explanations | `diagnosis_result`, `diagnosis_reason`, `diagnosis_rule_match` |
| Treatment engine | Rule-level treatments via `rule_treatment` (fallback: `disease_treatment`) |
| History export | Editable report fields + PDF via `consultation_report` |
| Consultation actor | `performed_by_user_id` (required) + optional `farmer_id` + `consultation_type` |
| Disease vs rule knowledge | `disease_symptom` (facts) separate from `rule_*` (logic) — see `ARCHITECTURE.md` |

---

## Admin pages

| Page | Purpose |
|------|---------|
| Dashboard | Statistics, disease frequency, recent diagnoses |
| Farmers | Add, edit, view farmer history |
| Diagnosis | Select farmer, crop, symptoms, conditions → result |
| History | All consultations, farmer filter, PDF export |
| Diseases | Add, edit disease knowledge |
| Symptoms | Reusable symptom CRUD (no disease linking here) |
| Treatments | Treatment CRUD |
| Rules | Central knowledge base (symptoms, conditions, treatments, confidence) |
| Reports | Disease, consultation, AI evaluation statistics |

## Farmer pages

| Page | Purpose |
|------|---------|
| Dashboard | Recent diagnoses, quick access |
| Diagnosis | Self-service diagnosis |
| My History | Own consultations, PDF download |
| Profile | Personal information |

---

## Demo accounts

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| farmer1 | farmer123 | Farmer |

---

## Database tables (final)

```
crop, disease, symptom, treatment
environmental_condition, environmental_condition_value
disease_symptom, disease_environment, disease_treatment
rule, rule_symptom, rule_environment, rule_treatment
role, app_user, farmer
consultation, consultation_symptom, consultation_environment, consultation_treatment
diagnosis_result, diagnosis_reason, diagnosis_reason_symptom
diagnosis_reason_environment, diagnosis_rule_match, reason_type
ai_prediction, consultation_report
```

**Principles:** no arrays, no JSON lists, one value per cell, foreign keys for all expert knowledge.

## Consultation types

| Type | performed_by | farmer_id | Meaning |
|------|--------------|-----------|---------|
| `FARMER_SELF` | Farmer user | Farmer profile | Farmer diagnoses himself |
| `ADMIN_FOR_FARMER` | Admin user | Selected farmer | Admin diagnoses for a farmer |
| `ADMIN_GENERAL` | Admin user | NULL | Admin test/general diagnosis |
