# Tomato Disease Expert System

AI-powered expert system for **tomato** disease diagnosis and treatment recommendation (CEF610 Final Practical Project).

## Design principles

- **Fully normalized PostgreSQL** — one value per cell
- **No arrays or JSON lists** in the database
- **Rules use foreign keys only** — symptoms and conditions linked via `rule_symptom` and `rule_environment`
- **Diagnosis explanations stored traceably** — `diagnosis_result`, `diagnosis_reason`, and junction tables

## Login (demo)

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin — full knowledge management |
| expert | expert123 | Crop expert — same admin access as above |
| farmer1 | farmer123 | Farmer — diagnosis and own history |

**Not in scope:** Settings, About, AI Model Management pages.

See `DESIGN.md` for the locked final architecture and `ARCHITECTURE.md` for the disease vs rule knowledge separation.

## Project structure

```
crop-disease-expert-system/
├── app/                    # Python application
│   ├── expert_system/      # Rule-based inference engine
│   ├── ai/                 # ML training and prediction
│   ├── repositories/       # Database access layer
│   ├── services/           # Business logic
│   └── ui/                 # Streamlit interface
├── database/
│   ├── migrations/         # 001–007 table creation scripts
│   ├── seeds/              # Reference data (tomato diseases, rules)
│   ├── queries/            # Reusable SQL queries
│   ├── schema.sql          # Migration index
│   ├── run_all.sql         # One-command DB setup
│   └── ERD.md              # Entity-relationship diagram
├── data/                   # Training datasets
├── reports/                # Evaluation and technical reports
└── tests/
```

## Setup

### 1. PostgreSQL

```bash
createdb crop_expert_system
```

### 2. Run SQL scripts

From the `database/` folder:

```bash
psql -U postgres -d crop_expert_system -f run_all.sql
```

Or run migrations and seeds individually in numeric order.

### 3. Python environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # then edit DB credentials
```

### 4. Launch UI

Use **one** of these (avoids `ModuleNotFoundError: No module named 'app'`):

```bash
python run.py
```

Or install the package once, then use Streamlit directly:

```bash
pip install -e .
streamlit run app/ui/streamlit_app.py
```

## Diagnosis explanation tables

| Table | Role |
|-------|------|
| `diagnosis_result` | Final disease, title, explanation, confidence |
| `diagnosis_reason` | Each "why" with `reason_type` FK |
| `diagnosis_reason_symptom` | Symptoms that supported the diagnosis |
| `diagnosis_reason_environment` | Environmental factors that supported it |
| `diagnosis_rule_match` | Expert rules that fired |

## Phases covered

| Phase | Location |
|-------|----------|
| Database design | `database/migrations/`, `database/ERD.md` |
| Knowledge base | `database/seeds/` |
| Inference engine | `app/expert_system/` |
| PostgreSQL integration | `app/repositories/`, `app/database.py` |
| AI prediction | `app/ai/` |
| Hybrid system | `app/services/diagnosis_service.py` + `app/ai/predict.py` |
| UI | `app/ui/` |
| Testing | `tests/` |

## Tests

```bash
pytest tests/ -k "not integration"
```

Integration tests require a seeded database:

```bash
pytest tests/ -m integration
```
