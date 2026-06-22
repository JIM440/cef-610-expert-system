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
Set-Location database
psql -U postgres -d crop_expert_system -f run_all.sql
Set-Location ..
```

### 3. Update an existing database

After pulling application changes, apply the SQL updates directly:

```powershell
psql -U postgres -d crop_expert_system -f database/apply_current_updates.sql
```

Alternatively, use the Python migration runner:

```powershell
python scripts/apply_schema_updates.py
```

Both commands safely apply the current idempotent schema updates, including the database-backed `expert` role.

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
  migrations/         Ordered schema changes
  seeds/              Tomato diseases, symptoms, rules, and treatments
  queries/            Reusable reporting queries
scripts/               Schema and Gemini verification commands
tests/                 Automated tests
```

## Tests

```powershell
python -m pytest -q
```

See `DESIGN.md`, `ARCHITECTURE.md`, and `database/SCHEMA_AUDIT.md` for implementation details.