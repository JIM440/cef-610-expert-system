# Schema Consolidation Audit

Audit date: 2026-06-21

## Applied

- `farmer.email` exists separately from the login username.
- Image diagnoses store `consultation.source`, `gemini_raw_extraction`, and
  `match_tier` through migration `015`.
- Image-extracted symptom IDs are stored in `consultation_symptom`.
- Migration `016` adds `matched` flags to `consultation_symptom` and
  `consultation_environment`.

## Not Consolidated

- Roles remain in a separate `role` table and `app_user.role_id` foreign key.
- Environmental factors remain split between `environmental_condition` and
  `environmental_condition_value`.
- Diagnosis details remain in `diagnosis_result`, `diagnosis_reason`, and
  `diagnosis_rule_match` tables.
- Random-forest comparison results remain in `ai_prediction`.

These legacy structures are still used by repositories, reports, seeds, and
history queries. They were not dropped because doing so would require a
separate data migration and coordinated repository rewrite. Removing them in
place would break existing installations and violate the non-destructive
migration requirement.
