# Entity-Relationship Diagram

The production schema contains exactly 15 application tables.

```mermaid
erDiagram
    app_user ||--o{ consultation : performs
    app_user ||--o{ consultation : owns
    crop ||--o{ disease : contains
    crop ||--o{ consultation : concerns
    disease ||--o{ disease_symptom : has
    symptom ||--o{ disease_symptom : describes
    disease ||--o{ rule : diagnosed_by
    disease ||--o{ consultation : result
    rule ||--o{ rule_symptom : requires
    symptom ||--o{ rule_symptom : participates
    rule ||--o{ rule_environment : requires
    environmental_factor ||--o{ rule_environment : participates
    rule ||--o{ rule_treatment : recommends
    treatment ||--o{ rule_treatment : participates
    rule ||--o{ consultation : matched
    consultation ||--o{ consultation_symptom : records
    symptom ||--o{ consultation_symptom : selected
    consultation ||--o{ consultation_environment : records
    environmental_factor ||--o{ consultation_environment : selected
    consultation ||--o{ consultation_treatment : recommends
    treatment ||--o{ consultation_treatment : selected
```

## Table groups

| Group | Tables |
|---|---|
| Users | `app_user` |
| Knowledge base | `crop`, `disease`, `symptom`, `treatment`, `environmental_factor`, `disease_symptom` |
| Expert rules | `rule`, `rule_symptom`, `rule_environment`, `rule_treatment` |
| Consultations | `consultation`, `consultation_symptom`, `consultation_environment`, `consultation_treatment` |

`database/schema.sql` is the canonical schema. `database/seed.sql` contains the current knowledge base and demo data.