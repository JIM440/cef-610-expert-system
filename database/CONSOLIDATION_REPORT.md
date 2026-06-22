# Database Consolidation Verification

Migration executed: 2026-06-22

The live `crop_expert_system` database was consolidated from 29 to 15 tables. The pre-migration backup is stored at `C:\tmp\crop_expert_pre_consolidation.dump`.

## Retained table counts

| Table | Before | After |
|---|---:|---:|
| `app_user` | 4 | 4 |
| `consultation` | 4 | 4 |
| `consultation_environment` | 5 | 5 |
| `consultation_symptom` | 30 | 30 |
| `consultation_treatment` | 8 | 8 |
| `crop` | 1 | 1 |
| `disease` | 8 | 8 |
| `disease_symptom` | 23 | 23 |
| `environmental_factor` | 15 source pairs | 15 |
| `rule` | 13 | 13 |
| `rule_environment` | 14 | 14 |
| `rule_symptom` | 20 | 20 |
| `rule_treatment` | 19 | 19 |
| `symptom` | 12 | 12 |
| `treatment` | 10 | 10 |

## Folded data

- Four role values were copied into `app_user.role`.
- Two farmer profiles were merged into their corresponding `app_user` records.
- Four diagnosis results were folded into `consultation`.
- Four matched rules and four explanations were retained on `consultation`.
- Eight matched symptom records were retained in `consultation_symptom.matched`.

## Approved dropped data

The user explicitly approved destructive migration. Six `disease_environment` rows and six `disease_treatment` rows that were not represented by expert rules were dropped. Legacy AI predictions, stored reports, image metadata, and diagnosis-reason chain tables had no independent retained records beyond the data folded into consultations.