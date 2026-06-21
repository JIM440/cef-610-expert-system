import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.user_repository import (
    create_farmer_with_account,
    get_all_farmers,
    update_farmer_record,
)
from app.services.consultation_service import ConsultationService
from app.utils.auth import require_admin

require_admin()
st.header("Farmers")

farmers = get_all_farmers()
search = st.text_input(
    "Search farmers",
    placeholder="Name, username, email, phone, or location...",
)
filtered = farmers
if search:
    query = search.casefold()
    filtered = [
        farmer
        for farmer in farmers
        if any(
            query in str(farmer.get(field) or "").casefold()
            for field in (
                "full_name",
                "username",
                "email",
                "phone_number",
                "location",
            )
        )
    ]

table_tab, edit_tab = st.tabs(["All farmers", "Edit/Add"])

with table_tab:
    if filtered:
        table = pd.DataFrame(filtered)[
            [
                "id",
                "full_name",
                "username",
                "email",
                "phone_number",
                "location",
                "account_active",
                "created_at",
            ]
        ]
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "full_name": "Farmer",
                "username": "Username",
                "email": "Email",
                "phone_number": "Phone",
                "location": "Location",
                "account_active": st.column_config.CheckboxColumn(
                    "Active account",
                    disabled=True,
                ),
                "created_at": st.column_config.DatetimeColumn(
                    "Registered",
                    format="MMM D, YYYY",
                ),
            },
        )
    else:
        st.info("No farmers match this search.")

with edit_tab:
    if farmers:
        with st.expander("Edit farmer", expanded=True):
            farmer_id = st.selectbox(
                "Farmer",
                [farmer["id"] for farmer in farmers],
                format_func=lambda selected_id: next(
                    farmer["full_name"]
                    for farmer in farmers
                    if farmer["id"] == selected_id
                ),
            )
            farmer = next(item for item in farmers if item["id"] == farmer_id)
            name = st.text_input(
                "Full name",
                value=farmer["full_name"],
                key="edit_name",
            )
            phone = st.text_input(
                "Phone",
                value=farmer["phone_number"] or "",
                key="edit_phone",
            )
            location = st.text_input(
                "Location",
                value=farmer["location"] or "",
                key="edit_loc",
            )
            email = st.text_input(
                "Email",
                value=farmer["email"] or "",
                key="edit_email",
            )
            if farmer.get("username"):
                st.caption(f"Login username: **{farmer['username']}**")
            else:
                st.warning("No login account linked to this farmer yet.")

            if st.button("Save farmer", type="primary"):
                update_farmer_record(farmer_id, name, phone, location, email)
                st.success("Farmer updated.")
                st.rerun()

            st.markdown("**Farmer history**")
            history = ConsultationService().get_history(farmer_id=farmer_id)
            if history:
                history_table = pd.DataFrame(
                    [
                        {
                            "Date": row["consultation_date"],
                            "Disease": row.get("diagnosed_disease") or "-",
                            "Confidence": row.get("confidence_score") or 0,
                            "Source": (
                                "Image"
                                if row.get("source") == "IMAGE"
                                else "Symptoms"
                            ),
                        }
                        for row in history
                    ]
                )
                st.dataframe(
                    history_table,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Date": st.column_config.DatetimeColumn(
                            "Date",
                            format="MMM D, YYYY",
                        ),
                        "Confidence": st.column_config.ProgressColumn(
                            "Confidence",
                            min_value=0,
                            max_value=100,
                            format="%d%%",
                        ),
                    },
                )
            else:
                st.caption("No consultations recorded for this farmer.")

    with st.expander("Add farmer and login", expanded=not farmers):
        st.caption("Creates a farmer profile and a login account in the database.")
        name = st.text_input("Full name", key="new_name")
        phone = st.text_input("Phone", key="new_phone")
        location = st.text_input("Location", key="new_loc")
        email = st.text_input("Email", key="new_email")
        username = st.text_input(
            "Username",
            key="new_username",
            placeholder="Unique login name",
        )
        password = st.text_input("Password", type="password", key="new_password")
        if st.button("Add farmer", type="primary"):
            if not all([name.strip(), username.strip(), password]):
                st.error("Full name, username, and password are required.")
            else:
                try:
                    create_farmer_with_account(
                        name.strip(),
                        phone,
                        location,
                        email,
                        username.strip(),
                        password,
                    )
                    st.success(
                        f"Farmer and login account '{username.strip()}' created."
                    )
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
                except Exception as exc:
                    st.error(f"Could not create farmer: {exc}")
