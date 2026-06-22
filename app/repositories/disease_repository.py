"""Disease facts retained in disease and disease_symptom.
Environmental and treatment displays are derived from expert rules.
"""

from app.database import execute, fetch_all, fetch_one
from .crop_repository import TOMATO_CROP_NAME


def get_diseases_by_crop(crop_id: int) -> list[dict]:
    return fetch_all("SELECT id,name,description,explanation_template,crop_id FROM disease WHERE crop_id=%(crop_id)s ORDER BY name", {"crop_id": crop_id})


def get_all_diseases() -> list[dict]:
    return fetch_all("""
        SELECT d.id,d.name,d.description,d.explanation_template
        FROM disease d JOIN crop c ON c.id=d.crop_id
        WHERE c.name=%(crop)s ORDER BY d.name
    """, {"crop": TOMATO_CROP_NAME})


def get_disease_by_id(disease_id: int) -> dict | None:
    return fetch_one("SELECT id,crop_id,name,description,explanation_template FROM disease WHERE id=%(id)s", {"id": disease_id})


def create_disease(crop_id: int, name: str, description: str, explanation_template: str) -> int:
    return execute("""
        INSERT INTO disease (crop_id,name,description,explanation_template)
        VALUES (%(crop_id)s,%(name)s,%(desc)s,%(template)s) RETURNING id
    """, {"crop_id":crop_id,"name":name,"desc":description,"template":explanation_template})


def update_disease(disease_id: int, name: str, description: str, explanation_template: str) -> None:
    execute("UPDATE disease SET name=%(name)s,description=%(desc)s,explanation_template=%(template)s WHERE id=%(id)s", {"id":disease_id,"name":name,"desc":description,"template":explanation_template})


def get_symptoms_for_disease(disease_id: int) -> list[dict]:
    return fetch_all("""
        SELECT s.id,s.name,s.description,ds.weight
        FROM disease_symptom ds JOIN symptom s ON s.id=ds.symptom_id
        WHERE ds.disease_id=%(id)s ORDER BY ds.weight DESC,s.name
    """, {"id": disease_id})


def link_disease_symptom(disease_id: int, symptom_id: int, weight: int = 1) -> None:
    execute("""
        INSERT INTO disease_symptom (disease_id,symptom_id,weight)
        VALUES (%(did)s,%(sid)s,%(weight)s)
        ON CONFLICT (disease_id,symptom_id) DO UPDATE SET weight=EXCLUDED.weight
    """, {"did":disease_id,"sid":symptom_id,"weight":weight})


def unlink_disease_symptom(disease_id: int, symptom_id: int) -> None:
    execute("DELETE FROM disease_symptom WHERE disease_id=%(did)s AND symptom_id=%(sid)s", {"did":disease_id,"sid":symptom_id})


def get_environments_for_disease(disease_id: int) -> list[dict]:
    return fetch_all("""
        SELECT DISTINCT ef.category AS condition_name, ef.value_name, 1 AS weight
        FROM rule r
        JOIN rule_environment re ON re.rule_id=r.id
        JOIN environmental_factor ef ON ef.id=re.environmental_factor_id
        WHERE r.disease_id=%(id)s
        ORDER BY ef.category,ef.value_name
    """, {"id": disease_id})


def get_treatments_for_disease(disease_id: int) -> list[dict]:
    return fetch_all("""
        SELECT t.id,t.name,t.description,MIN(rt.priority_level) AS priority_level
        FROM rule r JOIN rule_treatment rt ON rt.rule_id=r.id
        JOIN treatment t ON t.id=rt.treatment_id
        WHERE r.disease_id=%(id)s
        GROUP BY t.id,t.name,t.description
        ORDER BY MIN(rt.priority_level),t.name
    """, {"id": disease_id})


def get_disease_knowledge_summary(disease_id: int) -> dict | None:
    disease=get_disease_by_id(disease_id)
    if not disease: return None
    return {"disease":disease,"symptoms":get_symptoms_for_disease(disease_id),
            "environments":get_environments_for_disease(disease_id),
            "treatments":get_treatments_for_disease(disease_id)}


def delete_disease(disease_id: int) -> None:
    execute("DELETE FROM disease WHERE id=%(id)s", {"id":disease_id})
