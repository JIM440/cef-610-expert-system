# Tomato Disease Expert System

A Streamlit and PostgreSQL expert system for diagnosing tomato plant diseases and recommending treatments.

## How diagnosis works

1. A user selects tomato symptoms manually, or uploads a tomato plant image.
2. Gemini Vision extracts visible symptoms from the image.
3. Extracted symptom names are mapped to symptom records in PostgreSQL.
4. The rule-based inference engine evaluates the selected symptoms and environmental conditions.
5. The matched database rule determines the disease, confidence tier, explanation, and treatment.
6. The consultation and its matched evidence are stored for history and reporting.

Gemini does not make the final diagnosis. The database knowledge base and inference engine do.

## Demo accounts

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Administrator |
| `expert` | `expert123` | Crop expert |
| `farmer1` | `farmer123` | Farmer |

## Setup

### 1. Install dependencies

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Update `.env` with the PostgreSQL password and Gemini API key.

### 2. Create a fresh database

```powershell
createdb crop_expert_system
psql -U postgres -d crop_expert_system -f database/schema.sql
psql -U postgres -d crop_expert_system -f database/seed.sql
```

### 3. Consolidate a legacy database

Back up the database first, then run the reviewed one-time consolidation:

```powershell
pg_dump -U postgres -Fc crop_expert_system -f crop_expert_pre_consolidation.dump
psql -U postgres -d crop_expert_system -f database/consolidate_29_to_15.sql
```

### 4. Launch the application

```powershell
python run.py
```

## Project structure

```text
app/
  ai/                 Gemini image symptom extraction
  expert_system/      Rule matching and inference
  repositories/       PostgreSQL data access
  services/           Diagnosis and reporting workflows
  ui/                 Streamlit pages and components
database/
  schema.sql           Canonical 15-table PostgreSQL schema
  seed.sql             Current tomato knowledge base and demo data
  consolidate_29_to_15.sql  One-time legacy consolidation
scripts/               Gemini verification commands
tests/                 Automated tests
```

## Tests

```powershell
python -m pytest -q
```

See `DESIGN.md`, `ARCHITECTURE.md`, and `database/SCHEMA_AUDIT.md` for implementation details.