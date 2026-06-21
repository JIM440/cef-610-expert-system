import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.treatment_repository import (
    create_treatment,
    delete_treatment,
    get_all_treatments,
    update_treatment,
)
from app.utils.auth import require_admin

require_admin()
st.header("Treatments")

treatments = get_all_treatments()
search = st.text_input("Search treatments", placeholder="Name or description...")
filtered = treatments
if search:
    q = search.lower()
    filtered = [t for t in treatments if q in t["name"].lower() or q in (t.get("description") or "").lower()]

tab1, tab2 = st.tabs(["All treatments", "Edit/Add"])

with tab1:
    st.dataframe(
        pd.DataFrame(filtered),
        use_container_width=True,
        hide_index=True,
        column_config={"id": st.column_config.NumberColumn("ID", format="%d")},
    )

with tab2:
    if treatments:
        with st.expander("Edit treatment", expanded=True):
            tid = st.selectbox(
                "Treatment",
                [t["id"] for t in treatments],
                format_func=lambda i: next(t["name"] for t in treatments if t["id"] == i),
            )
            t = next(x for x in treatments if x["id"] == tid)
            name = st.text_input("Name", value=t["name"])
            desc = st.text_area("Description", value=t["description"] or "")
            c1, c2 = st.columns(2)
            if c1.button("Save", type="primary"):
                update_treatment(tid, name, desc)
                st.success("Updated.")
                st.rerun()
            confirm = c2.checkbox("Confirm delete", key=f"confirm_treatment_{tid}")
            if c2.button("Delete", disabled=not confirm):
                delete_treatment(tid)
                st.success("Deleted.")
                st.rerun()

    with st.expander("Add treatment", expanded=not treatments):
        name = st.text_input("Treatment name", key="new_treatment_name")
        desc = st.text_area("Description", key="new_treatment_desc")
        if st.button("Add treatment", type="primary"):
            create_treatment(name, desc)
            st.success("Treatment added.")
            st.rerun()
