# Schema Audit

Audit date: 2026-06-22

## Current application schema

- Login accounts are stored in `app_user` and reference database roles through `role`.
- Database roles include `admin`, `expert`, and `farmer`.
- The `expert` demo account is assigned to the `expert` role by migration `017`.
- Farmer profile data remains separate from login credentials.
- Manual and image diagnoses store their source, confidence tier, and matched evidence.
- Gemini-extracted symptoms are mapped to `symptom` records and stored in `consultation_symptom`.
- `consultation_symptom.matched` and `consultation_environment.matched` identify facts used by the selected rule.
- Diagnosis explanations remain traceable through `diagnosis_result`, `diagnosis_reason`, and `diagnosis_rule_match`.
- Editable PDF report content is stored in `consultation_report` before download.

## Deliberately normalized structures

- Environmental factors remain split between `environmental_condition` and `environmental_condition_value`.
- Disease facts and diagnosis rules remain separate: disease associations describe knowledge, while rule junction tables drive inference.
- Treatment recommendations can be linked to diseases generally and to individual rules with priority.

## Removed legacy path

The unused Random Forest training and prediction modules were removed. Gemini extracts image symptoms, while the database rule engine remains the only final diagnosis authority.