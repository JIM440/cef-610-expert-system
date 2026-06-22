import app.path_setup  # noqa: F401

import streamlit as st

from app.repositories.user_repository import create_farmer_with_account, get_all_farmers, update_farmer_record
from app.services.consultation_service import ConsultationService
from app.ui.components.farmer_theme import render_page_header
from app.utils.auth import require_expert

require_expert()
render_page_header("Farmers", "Manage farmer profiles and their database login accounts.")

farmers = get_all_farmers()
list_tab, edit_tab, add_tab = st.tabs(["Farmer cards", "Edit farmer", "+ Add farmer"])

with list_tab:
    search = st.text_input("Search farmers", placeholder="Name, username, email, phone, or location...")
    q = search.casefold().strip()
    filtered = [f for f in farmers if not q or any(q in str(f.get(k) or "").casefold() for k in ("full_name", "username", "email", "phone_number", "location"))]
    if not filtered:
        st.info("No farmers match this search.")
    for start in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, farmer in zip(cols, filtered[start:start + 3]):
            with col:
                with st.container(border=True):
                    st.subheader(farmer["full_name"])
                    st.caption(f"@{farmer.get('username') or 'no-login'}")
                    st.write(f"**Email:** {farmer.get('email') or '-'}")
                    st.write(f"**Phone:** {farmer.get('phone_number') or '-'}")
                    st.write(f"**Location:** {farmer.get('location') or '-'}")
                    created = farmer.get("created_at")
                    st.caption(f"Registered {created.strftime('%b %d, %Y') if hasattr(created, 'strftime') else str(created)[:10]}")

with edit_tab:
    if not farmers:
        st.info("Add a farmer first.")
    else:
        farmer_id = st.selectbox("Select farmer", [f["id"] for f in farmers], format_func=lambda i: next(f["full_name"] for f in farmers if f["id"] == i))
        farmer = next(f for f in farmers if f["id"] == farmer_id)
        with st.form("edit_farmer_form"):
            name = st.text_input("Full name", value=farmer["full_name"])
            phone = st.text_input("Phone", value=farmer.get("phone_number") or "")
            location = st.text_input("Location", value=farmer.get("location") or "")
            email = st.text_input("Email", value=farmer.get("email") or "")
            st.text_input("Login username", value=farmer.get("username") or "No linked login", disabled=True)
            save = st.form_submit_button("Save farmer", type="primary", width="stretch")
        if save:
            if not name.strip():
                st.error("Full name is required.")
            else:
                update_farmer_record(farmer_id, name.strip(), phone.strip(), location.strip(), email.strip())
                st.success("Farmer updated.")
                st.rerun()

        st.markdown("**Consultation history**")
        history = ConsultationService().get_history(farmer_id=farmer_id)
        if not history:
            st.caption("No consultations recorded for this farmer.")
        for row in history[:8]:
            with st.container(border=True):
                c1, c2 = st.columns([2, 1])
                c1.write(f"**{row.get('diagnosed_disease') or 'No diagnosis'}**")
                c1.caption(row.get("symptoms") or "No symptoms recorded")
                c2.metric("Confidence", f"{row.get('confidence_score') or 0}%")
                c2.caption("Image" if row.get("source") == "IMAGE" else "Manual")

with add_tab:
    st.markdown("**Create farmer profile and login**")
    with st.form("add_farmer_form"):
        name = st.text_input("Full name")
        phone = st.text_input("Phone")
        location = st.text_input("Location")
        email = st.text_input("Email")
        username = st.text_input("Username", placeholder="Unique login name")
        password = st.text_input("Password", type="password")
        add = st.form_submit_button("Add farmer", type="primary", width="stretch")
    if add:
        if not all([name.strip(), username.strip(), password]):
            st.error("Full name, username, and password are required.")
        else:
            try:
                create_farmer_with_account(name.strip(), phone.strip(), location.strip(), email.strip(), username.strip(), password)
                st.success(f"Farmer and login '{username.strip()}' created.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not create farmer: {exc}")