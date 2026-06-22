# Schema Audit

Audit date: 2026-06-22

## Result

- The live PostgreSQL database contains exactly 15 public application tables.
- `app_user` stores login credentials, roles, and farmer profile data.
- Roles are constrained values on `app_user.role`: `ADMIN`, `EXPERT`, or `FARMER`.
- `environmental_factor` replaces the former condition/value table pair.
- The final diagnosis, confidence, matched rule, and explanation are stored on `consultation`.
- Gemini is used only to extract visible tomato symptoms. Final diagnosis remains database rule-driven.
- Reports are generated on demand from consultation data and are not persisted.
- No migration-tracking table is present.

## Canonical database files

| File | Purpose |
|---|---|
| `schema.sql` | Exact 15-table schema |
| `seed.sql` | Current knowledge base, demo users, and retained consultation data |
| `consolidate_29_to_15.sql` | Reviewed one-time migration from the legacy schema |
| `CONSOLIDATION_REPORT.md` | Pre/post row-count verification |

The obsolete migration, seed-fragment, and query folders were removed after consolidation.