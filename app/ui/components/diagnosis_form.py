import streamlit as st

from app.ai.predict import predict_disease
from app.repositories.crop_repository import get_tomato_crop_id
from app.repositories.symptom_repository import get_all_symptoms, get_environmental_conditions
from app.repositories.user_repository import get_all_farmers
from app.services.diagnosis_service import DiagnosisService
from app.ui.components.result_card import render_diagnosis_result
from app.ui.components.symptom_selector import render_environment_selector, render_symptom_selector
from app.utils.auth import current_user, is_admin
from app.utils.consultation_types import LABELS
from app.utils.helpers import format_confidence
from app.utils.validators import require_non_empty_selection


def render_diagnosis_page(
    farmer_id: int | None = None,
    allow_farmer_select: bool = False,
) -> None:
    user = current_user()
    if not user:
        st.error("Not logged in.")
        st.stop()

    crop_id = get_tomato_crop_id()
    if crop_id is None:
        st.warning("Tomato crop is not configured in the database.")
        st.stop()

    selected_farmer_id = farmer_id
    if allow_farmer_select and is_admin():
        mode = st.radio(
            "Diagnosis mode",
            [
                "General diagnosis (not for a specific farmer)",
                "Diagnosis for a specific farmer",
            ],
        )
        if mode.startswith("Diagnosis for"):
            farmers = get_all_farmers()
            if not farmers:
                st.warning("No farmers registered.")
                st.stop()
            farmer_options = {f["full_name"]: f["id"] for f in farmers}
            choice = st.selectbox("Select farmer", list(farmer_options.keys()))
            selected_farmer_id = farmer_options[choice]
        else:
            selected_farmer_id = None
            st.caption("This consultation will be recorded as ADMIN_GENERAL with no farmer attached.")

    symptoms = get_all_symptoms()
    selected_symptom_ids = render_symptom_selector(symptoms)
    env_rows = get_environmental_conditions()
    selected_condition_ids = render_environment_selector(env_rows)

    if st.button("Run diagnosis", type="primary"):
        error = require_non_empty_selection("symptom", selected_symptom_ids)
        if error:
            st.error(error)
            return

        service = DiagnosisService()
        ctype, target_farmer_id = service.resolve_consultation_type(
            is_admin=is_admin(),
            farmer_id=selected_farmer_id if allow_farmer_select else farmer_id,
            actor_farmer_id=user.get("farmer_id"),
        )

        result = service.run_diagnosis(
            crop_id=crop_id,
            symptom_ids=selected_symptom_ids,
            condition_value_ids=selected_condition_ids,
            performed_by_user_id=user["id"],
            consultation_type=ctype,
            farmer_id=target_farmer_id,
        )
        if not result:
            st.warning("No matching expert rules found.")
            return

        st.success(f"Diagnosis saved automatically ({LABELS.get(ctype, ctype)}).")

        ai_result = predict_disease(
            result["consultation_id"],
            selected_symptom_ids,
            selected_condition_ids,
        )
        if ai_result:
            st.info(f"AI prediction confidence: {format_confidence(ai_result['confidence'])}")
        render_diagnosis_result(result)
