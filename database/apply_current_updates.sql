-- Apply current idempotent updates to an existing database.
-- Run from any directory with:
-- psql -U postgres -d crop_expert_system -f database/apply_current_updates.sql

\ir migrations/015_consultation_source_match_tier.sql
\ir migrations/016_consultation_match_trace.sql
\ir migrations/017_create_expert_role.sql

\echo 'Current database updates applied successfully.'
