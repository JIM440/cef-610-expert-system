# Disease Knowledge vs Rule Knowledge

This is one of the most important architectural decisions in the project. Many student projects combine these into a single table. It works initially, but becomes hard to maintain. Separating them mirrors how real expert systems are built.

---

## The difference

| Layer | Question | Nature |
|-------|----------|--------|
| **Disease Knowledge** | What do we know about a disease? | **Facts** |
| **Rule Knowledge** | When should the system conclude this disease exists? | **Reasoning** |

### Disease knowledge = facts

```text
Early Blight commonly causes:
- Yellow Leaves
- Brown Spots
- Leaf Drop
```

Nobody is making a diagnosis yet. We are stating: *these symptoms are associated with this disease.*

### Rule knowledge = reasoning

```text
IF Yellow Leaves AND Brown Spots AND High Humidity
THEN Early Blight (Confidence = 85%)
```

The system is making a **decision**.

---

## Real-world analogy

A doctor knows fever is associated with malaria, typhoid, flu, and COVID — that is **disease knowledge**.

But the doctor reasons: *IF fever AND headache AND chills THEN possible malaria* — that is **rule knowledge**.

---

## Disease knowledge tables

| Table | Role |
|-------|------|
| `disease` | Disease entities |
| `symptom` | Reusable symptom entities |
| `disease_symptom` | Factual symptom associations |
| `disease_environment` | Factual environmental associations |
| `disease_treatment` | General treatments linked to disease |

`disease_symptom` does **not** mean “diagnose the disease.” It means “these symptoms are known to occur with this disease.”

### Why keep disease_symptom?

The **Diseases** page and disease detail views need it:

```text
Early Blight
Common Symptoms:
- Yellow Leaves
- Brown Spots
- Leaf Drop
```

Without `disease_symptom`, the disease knowledge UI is impossible.

---

## Rule knowledge tables

| Table | Role |
|-------|------|
| `rule` | Diagnostic rule linked to one disease |
| `rule_symptom` | Symptoms **required** for this rule to fire |
| `rule_environment` | Conditions **required** for this rule |
| `rule_treatment` | Treatments recommended when this rule matches |

---

## Why not use disease_symptom for diagnosis?

Not every associated symptom is required for diagnosis.

**Early Blight** may be associated with:

- Yellow Leaves
- Brown Spots
- Leaf Drop

But a rule might only require:

- Brown Spots
- Yellow Leaves
- High Humidity

`Leaf Drop` is associated with the disease but **not required** by the rule. That is why the tables stay separate.

### Example in our seed data

| Knowledge | Early Blight |
|-----------|--------------|
| `disease_symptom` | Brown spots, Yellowing, **Leaf drop** |
| `EB-Rule-01` requires | Brown spots, Yellowing, High humidity |

Leaf drop appears in facts but not in the rule — exactly as designed.

---

## Benefits during diagnosis

**Farmer selects:** Yellow Leaves, Brown Spots

| Component | Reads from | Result |
|-----------|------------|--------|
| Inference engine | `rule_symptom` | Rule matched |
| Disease detail / result card | `disease_symptom` | Shows all common symptoms, marks which were observed |

Different tables, different purpose.

---

## Benefits during AI training

```text
Disease Knowledge  →  AI learns disease ↔ symptom relationships
Rule Knowledge     →  Expert system reasoning layer
                              ↓
                      Hybrid Diagnosis
                              ↓
                        Treatments
```

```text
                Symptoms
                     ↓
          ┌──────────────────┐
          │ Expert System    │
          │ (Rules)          │
          └──────────────────┘
                     ↓
          ┌──────────────────┐
          │ AI Predictor     │
          └──────────────────┘
                     ↓
          Hybrid Diagnosis
                     ↓
               Treatments
```

---

## Repository separation

### `DiseaseRepository`

Manages: `disease`, `disease_symptom`, `disease_environment`, `disease_treatment`

Used by: Diseases page, disease details, knowledge base, reports, AI training context

### `RuleRepository`

Manages: `rule`, `rule_symptom`, `rule_environment`, `rule_treatment`

Used by: `InferenceEngine`, diagnosis service, confidence calculator, explanation builder

**The inference engine never reads `disease_symptom` for matching.**

---

## Final principle

```text
Disease Knowledge → "What is true about this disease?"
Rule Knowledge    → "When should I diagnose this disease?"
```

This separation supports the Expert System phase, the AI phase, and the Hybrid phase without redesigning the database.
