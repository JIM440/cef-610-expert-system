# Final System Design

## Scope

The system supports tomato disease diagnosis through manual symptom selection and Gemini image symptom extraction. Gemini identifies visible evidence only; the PostgreSQL expert rules make the final diagnosis and select treatments.

## Roles and pages

| Role | Pages |
|---|---|
| Expert | Dashboard, Diagnosis, History, Image Recognition, Experts, Farmers, Diseases, Symptoms, Treatments, Expert Rules |
| Farmer | Dashboard, Diagnosis, History, Image Recognition |

Experts and farmers are stored in `app_user`. A farmer diagnosis is always saved as that farmer's own consultation. Experts can run general consultations or select a farmer.

## Database design

The final database contains 15 tables:

```text
app_user
crop, disease, symptom, treatment, environmental_factor, disease_symptom
rule, rule_symptom, rule_environment, rule_treatment
consultation, consultation_symptom, consultation_environment, consultation_treatment
```

The diagnosis result is stored directly on `consultation` using `final_disease_id`, `final_confidence`, `matched_rule_id`, and `explanation`. Reports are generated on demand and are not stored in a report table.

## Consultation types

| Type | Meaning |
|---|---|
| `FARMER_SELF` | Farmer diagnoses their own tomato plant |
| `ADMIN_FOR_FARMER` | Expert performs a diagnosis for a selected farmer |
| `ADMIN_GENERAL` | Expert performs a general/test diagnosis |
| `IMAGE_FARMER_SELF` | Farmer image-assisted self diagnosis |
| `IMAGE_ADMIN_FOR_FARMER` | Expert image-assisted diagnosis for a farmer |
| `IMAGE_ADMIN_GENERAL` | Expert general image-assisted diagnosis |

## Core constraints

- No arrays or JSON knowledge fields.
- One relationship per junction-table row.
- All symptoms, treatments, diseases, environmental factors, users, and rules come from PostgreSQL.
- Rule confidence is stored on `rule.confidence_score`.
- Uploaded images are not persisted in the database.