import streamlit as st

from app.config import GEMINI_CONFIG
from app.repositories.crop_repository import get_tomato_crop_id
from app.repositories.user_repository import get_all_farmers
from app.services.image_recognition_service import ImageRecognitionService
from app.ui.components.diagnosis_results_view import render_diagnosis_results_cards
from app.ui.components.farmer_theme import render_page_header
from app.ui.components.farmer_diagnosis import PREFILL_KEY
from app.utils.auth import is_admin, require_login

MAX_BYTES = 5 * 1024 * 1024
RESULT_KEY = "image_recognition_result"


def _continue_to_manual(symptom_ids: list[int]) -> None:
    st.session_state[PREFILL_KEY] = symptom_ids
    target = "pages/admin/diagnosis.py" if is_admin() else "pages/farmer/diagnosis.py"
    try:
        st.switch_page(target)
    except Exception:
        st.success("Symptoms are ready. Open the Diagnosis page to continue manually.")


def render_image_recognition_page(allow_farmer_select: bool = False) -> None:
    user = require_login()

    render_page_header(
        "Image Recognition",
        "Upload a clear image of the affected plant part. Gemini extracts symptoms; the expert system rule base performs the diagnosis.",
    )

    if not GEMINI_CONFIG.is_configured:
        st.error(
            "Image recognition requires a Gemini API key. "
            "Add `GEMINI_API_KEY` to your `.env` file and restart the app."
        )
        st.stop()

    if RESULT_KEY in st.session_state:
        payload = st.session_state[RESULT_KEY]
        analysis = payload["analysis"]
        st.subheader("Analysis results")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            with st.container(border=True):
                st.markdown("**Gemini visual summary**")
                st.write(analysis.get("visual_summary") or "No visual summary returned.")
        with col_b:
            with st.container(border=True):
                st.markdown("**Extracted symptoms**")
                if analysis["detected_symptoms"]:
                    for item in analysis["detected_symptoms"]:
                        st.checkbox(
                            f"{item['symptom_name']} ({item['score']}%)",
                            value=True,
                            disabled=True,
                            key=f"img_sym_{item['symptom_id']}",
                        )
                else:
                    st.caption("No symptoms matched the database catalog.")

        if payload.get("diagnosis"):
            render_diagnosis_results_cards(
                payload["diagnosis"],
                saved_note="Image diagnosis saved to history with source Image.",
            )
        elif analysis.get("detected_symptoms"):
            st.warning("Visual symptoms were found, but no expert rule could be scored from them.")
            if st.button(
                "Continue to manual diagnosis with these symptoms",
                type="primary",
                use_container_width=True,
            ):
                _continue_to_manual(analysis.get("symptom_ids", []))
        else:
            st.info("Try another image or continue with manual symptom selection.")

        if st.button("Analyze another image"):
            st.session_state.pop(RESULT_KEY, None)
            st.rerun()
        return

    col_upload, col_help = st.columns([1.2, 1])

    with col_upload:
        with st.container(border=True):
            st.markdown("**Upload plant image**")
            uploaded = st.file_uploader(
                "Upload plant image",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
            )
            st.caption("JPG, PNG, JPEG. Max 5MB. Images are sent to Gemini and are not stored.")

            if uploaded:
                if uploaded.size > MAX_BYTES:
                    st.error("File exceeds 5MB limit.")
                    st.stop()
                st.image(uploaded, caption="Uploaded image", use_container_width=True)

    with col_help:
        with st.container(border=True):
            st.markdown("**How it works**")
            st.write("1. Upload a clear image of the affected leaf, stem, or fruit.")
            st.write("2. Gemini identifies visible symptoms from the database catalog.")
            st.write("3. Expert rules match those symptoms to disease and treatment records.")
            st.write("4. The consultation stores text only: source and Gemini extraction, not the image file.")

    crop_id = get_tomato_crop_id()
    if crop_id is None:
        st.warning("Tomato crop is not configured in the database.")
        st.stop()

    target_farmer_id = user.get("farmer_id")
    if allow_farmer_select and is_admin():
        mode = st.radio(
            "Record diagnosis for",
            ["General (no farmer)", "Specific farmer"],
            horizontal=True,
        )
        if mode == "Specific farmer":
            farmers = get_all_farmers()
            if farmers:
                target_farmer_id = st.selectbox(
                    "Farmer",
                    [f["id"] for f in farmers],
                    format_func=lambda i: next(f["full_name"] for f in farmers if f["id"] == i),
                )
        else:
            target_farmer_id = None

    if uploaded and st.button("Analyze Image", type="primary", use_container_width=True):
        service = ImageRecognitionService()
        ctype, fid = service.resolve_image_consultation_type(
            is_admin=is_admin(),
            farmer_id=target_farmer_id if allow_farmer_select else user.get("farmer_id"),
            actor_farmer_id=user.get("farmer_id"),
        )

        with st.spinner("Sending image to Gemini and running expert rules..."):
            try:
                payload = service.analyze_and_diagnose(
                    image_bytes=uploaded.getvalue(),
                    original_filename=uploaded.name,
                    performed_by_user_id=user["id"],
                    consultation_type=ctype,
                    farmer_id=fid,
                    crop_id=crop_id,
                )
            except RuntimeError as exc:
                st.error(str(exc))
                return
            except Exception as exc:
                st.error(f"Image analysis failed: {exc}")
                return

        if not payload:
            st.error("Could not analyze image. Please try a clearer photo.")
            return

        st.session_state[RESULT_KEY] = payload
        st.rerun()

    elif not uploaded:
        st.info("Choose an image, then click Analyze Image.")
