import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.symptom_repository import (
    create_symptom,
    delete_symptom,
    get_all_symptoms,
    update_symptom,
)
from app.utils.auth import require_admin

require_admin()
st.header("Symptoms")
st.caption(
    "Reusable symptom entities only. Disease page links associated facts; Rules page links diagnosis requirements."
)

symptoms = get_all_symptoms()
search = st.text_input("Search symptoms", placeholder="Name or description...")
filtered = symptoms
if search:
    q = search.lower()
    filtered = [s for s in symptoms if q in s["name"].lower() or q in (s.get("description") or "").lower()]

tab1, tab2 = st.tabs(["All symptoms", "Edit/Add"])

with tab1:
    st.dataframe(
        pd.DataFrame(filtered),
        width="stretch",
        hide_index=True,
        column_config={"id": st.column_config.NumberColumn("ID", format="%d")},
    )

with tab2:
    if symptoms:
        with st.expander("Edit symptom", expanded=True):
            sid = st.selectbox(
                "Symptom",
                [s["id"] for s in symptoms],
                format_func=lambda i: next(s["name"] for s in symptoms if s["id"] == i),
            )
            s = next(x for x in symptoms if x["id"] == sid)
            name = st.text_input("Name", value=s["name"])
            desc = st.text_area("Description", value=s["description"] or "")
            c1, c2 = st.columns(2)
            if c1.button("Save", type="primary"):
                update_symptom(sid, name, desc)
                st.success("Updated.")
                st.rerun()
            confirm = c2.checkbox("Confirm delete", key=f"confirm_symptom_{sid}")
            if c2.button("Delete", disabled=not confirm):
                delete_symptom(sid)
                st.success("Deleted.")
                st.rerun()

    with st.expander("Add symptom", expanded=not symptoms):
        name = st.text_input("Symptom name", key="new_symptom_name")
        desc = st.text_area("Description", key="new_symptom_desc")
        if st.button("Add symptom", type="primary"):
            create_symptom(name, desc)
            st.success("Symptom added.")
            st.rerun()
