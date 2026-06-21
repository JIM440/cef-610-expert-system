import streamlit as st

from app.ai.predict import predict_disease
from app.repositories.crop_repository import get_tomato_crop_id
from app.repositories.symptom_repository import get_all_symptoms, get_environmental_conditions
from app.repositories.user_repository import get_all_farmers
from app.services.diagnosis_service import DiagnosisService
from app.ui.components.farmer_theme import render_page_header
from app.ui.components.diagnosis_results_view import render_diagnosis_results_cards
from app.utils.auth import is_admin, require_login
from app.utils.validators import require_non_empty_selection

PREFILL_KEY = "manual_diagnosis_prefill_symptom_ids"


def _render_stepper(step: int) -> None:
    s1 = "done" if step > 1 else "active"
    s2 = "active" if step == 2 else ""
    st.markdown(
        f"""
        <div class="stepper">
            <div class="step {s1}"><span class="step-num">{'✓' if step > 1 else '1'}</span> Information</div>
            <div style="flex:1;height:2px;background:#dce6df;"></div>
            <div class="step {s2}"><span class="step-num">2</span> Results</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _group_symptoms(symptoms: list[dict]) -> dict[str, list[dict]]:
    groups = {
        "Leaf symptoms": [],
        "Stem and plant symptoms": [],
        "Fruit symptoms": [],
        "Other symptoms": [],
    }
    for symptom in symptoms:
        text = f"{symptom['name']} {symptom.get('description') or ''}".lower()
        if any(word in text for word in ("leaf", "leaves", "yellow", "spot", "wilting")):
            groups["Leaf symptoms"].append(symptom)
        elif any(word in text for word in ("stem", "plant", "growth")):
            groups["Stem and plant symptoms"].append(symptom)
        elif any(word in text for word in ("fruit", "tomato")):
            groups["Fruit symptoms"].append(symptom)
        else:
            groups["Other symptoms"].append(symptom)
    return {name: items for name, items in groups.items() if items}


def _render_symptom_checkboxes(symptoms: list[dict], key_prefix: str) -> list[int]:
    st.markdown("**1. Select symptoms**")
    prefilled = set(st.session_state.pop(PREFILL_KEY, []))
    selected: list[int] = []
    groups = _group_symptoms(symptoms)
    for idx, (group_name, group_symptoms) in enumerate(groups.items()):
        with st.expander(group_name, expanded=idx == 0 or bool(prefilled & {s["id"] for s in group_symptoms})):
            cols = st.columns(2)
            for i, symptom in enumerate(group_symptoms):
                key = f"{key_prefix}_sym_{symptom['id']}"
                if symptom["id"] in prefilled:
                    st.session_state[key] = True
                with cols[i % 2]:
                    if st.checkbox(symptom["name"], key=key, help=symptom.get("description") or None):
                        selected.append(symptom["id"])
    return selected


def _render_environment_selectors(env_rows: list[dict], key_prefix: str) -> list[int]:
    st.markdown("**2. Environmental conditions (optional)**")
    conditions: dict[str, list[dict]] = {}
    for row in env_rows:
        conditions.setdefault(row["condition_name"], []).append(row)

    selected: list[int] = []
    cols = st.columns(2)
    for idx, (condition_name, values) in enumerate(conditions.items()):
        options = {v["value_name"]: v["value_id"] for v in values}
        with cols[idx % 2]:
            choice = st.selectbox(
                condition_name,
                ["Not specified"] + list(options.keys()),
                key=f"{key_prefix}_env_{condition_name}",
            )
            if choice in options:
                selected.append(options[choice])
    return selected


def _render_farmer_selector(key_prefix: str) -> int | None:
    mode = st.radio(
        "Record diagnosis for",
        ["General (no farmer)", "Specific farmer"],
        horizontal=True,
        key=f"{key_prefix}_farmer_mode",
    )
    if mode == "Specific farmer":
        farmers = get_all_farmers()
        if not farmers:
            st.warning("No farmers registered.")
            st.stop()
        return st.selectbox(
            "Select farmer",
            [f["id"] for f in farmers],
            format_func=lambda i: next(f["full_name"] for f in farmers if f["id"] == i),
            key=f"{key_prefix}_farmer_pick",
        )
    st.caption("This consultation will be stored as a general diagnosis.")
    return None


def render_farmer_diagnosis(
    farmer_id: int | None,
    allow_farmer_select: bool = False,
    key_prefix: str = "farmer",
) -> None:
    user = require_login()

    step_key = f"{key_prefix}_diag_step"
    result_key = f"{key_prefix}_diag_result"

    if step_key not in st.session_state:
        st.session_state[step_key] = 1

    render_page_header(
        "New Diagnosis" if st.session_state[step_key] == 1 else "Diagnosis Results",
        "Describe tomato symptoms to get a diagnosis."
        if st.session_state[step_key] == 1
        else "Review the diagnosis below.",
    )

    target_farmer_id = farmer_id
    if allow_farmer_select and is_admin() and st.session_state[step_key] == 1:
        target_farmer_id = _render_farmer_selector(key_prefix)

    _render_stepper(st.session_state[step_key])

    if st.session_state[step_key] == 2 and result_key in st.session_state:
        if st.button("Back", type="secondary"):
            st.session_state[step_key] = 1
            st.session_state.pop(result_key, None)
            st.rerun()
        render_diagnosis_results_cards(st.session_state[result_key])
        return

    crop_id = get_tomato_crop_id()
    if crop_id is None:
        st.warning("Tomato crop is not configured in the database.")
        st.stop()

    col_left, col_right = st.columns([1.25, 1])
    with col_left:
        symptoms = get_all_symptoms()
        selected_symptom_ids = _render_symptom_checkboxes(symptoms, key_prefix)

    with col_right:
        env_rows = get_environmental_conditions()
        selected_condition_ids = _render_environment_selectors(env_rows, key_prefix)

    if st.button("Get Diagnosis", type="primary", use_container_width=True):
        error = require_non_empty_selection("symptom", selected_symptom_ids)
        if error:
            st.error(error)
            return

        service = DiagnosisService()
        ctype, resolved_farmer_id = service.resolve_consultation_type(
            is_admin=is_admin() and allow_farmer_select,
            farmer_id=target_farmer_id if allow_farmer_select else farmer_id,
            actor_farmer_id=user.get("farmer_id"),
        )
        result = service.run_diagnosis(
            crop_id=crop_id,
            symptom_ids=selected_symptom_ids,
            condition_value_ids=selected_condition_ids,
            performed_by_user_id=user["id"],
            consultation_type=ctype,
            farmer_id=resolved_farmer_id,
        )
        if not result:
            st.warning("No expert rule could be scored for these symptoms.")
            return

        predict_disease(
            result["consultation_id"],
            selected_symptom_ids,
            selected_condition_ids,
        )

        st.session_state[result_key] = result
        st.session_state[step_key] = 2
        st.rerun()
