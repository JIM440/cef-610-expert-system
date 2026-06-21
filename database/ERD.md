# Entity-Relationship Diagram (Final)

```mermaid
erDiagram
    role ||--o{ app_user : has
    farmer ||--o{ app_user : linked_to
    farmer ||--o{ consultation : requests
    crop ||--o{ disease : has
    disease ||--o{ disease_symptom : links
    symptom ||--o{ disease_symptom : links
    disease ||--o{ disease_treatment : links
    treatment ||--o{ disease_treatment : links
    disease ||--o{ rule : defines
    rule ||--o{ rule_symptom : requires
    rule ||--o{ rule_environment : requires
    rule ||--o{ rule_treatment : recommends
    treatment ||--o{ rule_treatment : linked
    consultation ||--o{ diagnosis_result : produces
    diagnosis_result ||--o{ diagnosis_reason : explains
    diagnosis_result ||--o{ diagnosis_rule_match : matched
    consultation ||--o{ consultation_report : exports
    consultation ||--o{ ai_prediction : predicts
```

## Key separation

| Layer | Tables | Stores |
|-------|--------|--------|
| Disease knowledge | `disease_symptom`, `disease_environment` | Factual relationships |
| Rule knowledge | `rule_symptom`, `rule_environment`, `rule_treatment` | Diagnostic logic + treatments |
| Explanations | `diagnosis_result`, `diagnosis_reason`, `diagnosis_rule_match` | Result + traceable reasons |

## SQL script locations

| Folder | Purpose |
|--------|---------|
| `migrations/001`–`010` | Schema creation |
| `seeds/001`–`008` | Reference data + demo users |
| `queries/` | Reusable SELECT queries |
| `run_all.sql` | Full setup |
