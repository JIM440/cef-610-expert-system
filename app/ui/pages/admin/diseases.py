import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.crop_repository import get_tomato_crop_id
from app.repositories.disease_repository import (
    create_disease,
    delete_disease,
    get_all_diseases,
    get_disease_knowledge_summary,
    link_disease_symptom,
    link_disease_treatment,
    unlink_disease_symptom,
    update_disease,
)
from app.repositories.symptom_repository import get_all_symptoms
from app.repositories.treatment_repository import get_all_treatments
from app.utils.auth import require_admin

require_admin()
st.header("Diseases - Knowledge Base (Facts)")
st.caption(
    "Disease knowledge answers: What is true about this disease? Diagnosis logic lives on the Rules page."
)

diseases = get_all_diseases()
search = st.text_input("Search diseases", placeholder="Name or description...")
filtered = diseases
if search:
    q = search.lower()
    filtered = [d for d in diseases if q in d["name"].lower() or q in (d.get("description") or "").lower()]

tab1, tab2 = st.tabs(["Diseases", "Edit/Add"])

with tab1:
    st.dataframe(
        pd.DataFrame(filtered),
        use_container_width=True,
        hide_index=True,
        column_config={"id": st.column_config.NumberColumn("ID", format="%d")},
    )

with tab2:
    if diseases:
        with st.expander("Edit disease", expanded=True):
            did = st.selectbox(
                "Disease",
                [d["id"] for d in diseases],
                format_func=lambda i: next(d["name"] for d in diseases if d["id"] == i),
            )
            summary = get_disease_knowledge_summary(did)
            d = summary["disease"]
            name = st.text_input("Name", value=d["name"])
            desc = st.text_area("Description", value=d["description"] or "")
            template = st.text_area("Explanation template", value=d["explanation_template"] or "")
            c1, c2 = st.columns(2)
            if c1.button("Save disease info", type="primary"):
                update_disease(did, name, desc, template)
                st.success("Disease updated.")
                st.rerun()
            confirm = c2.checkbox("Confirm delete", key=f"confirm_disease_{did}")
            if c2.button("Delete disease", disabled=not confirm):
                delete_disease(did)
                st.success("Disease deleted.")
                st.rerun()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Common symptoms**")
                for s in summary["symptoms"]:
                    st.write(f"- {s['name']} (weight {s['weight']})")
                all_symptoms = get_all_symptoms()
                linked_ids = {s["id"] for s in summary["symptoms"]}
                available = [s for s in all_symptoms if s["id"] not in linked_ids]
                if available:
                    to_link = st.selectbox(
                        "Link symptom to disease",
                        [s["id"] for s in available],
                        format_func=lambda i: next(s["name"] for s in available if s["id"] == i),
                        key="link_symptom",
                    )
                    weight = st.number_input("Association weight", 1, 10, 1, key="sym_weight")
                    if st.button("Link symptom"):
                        link_disease_symptom(did, to_link, weight)
                        st.rerun()
                if summary["symptoms"]:
                    to_unlink = st.selectbox(
                        "Remove symptom link",
                        [s["id"] for s in summary["symptoms"]],
                        format_func=lambda i: next(s["name"] for s in summary["symptoms"] if s["id"] == i),
                        key="unlink_symptom",
                    )
                    if st.button("Unlink symptom"):
                        unlink_disease_symptom(did, to_unlink)
                        st.rerun()

            with col2:
                st.markdown("**Common environments**")
                for e in summary["environments"]:
                    st.write(f"- {e['condition_name']}: {e['value_name']}")

                st.markdown("**General treatments**")
                for t in summary["treatments"]:
                    st.write(f"- {t['name']}")
                all_treatments = get_all_treatments()
                linked_t = {t["id"] for t in summary["treatments"]}
                avail_t = [t for t in all_treatments if t["id"] not in linked_t]
                if avail_t:
                    tid = st.selectbox(
                        "Link treatment",
                        [t["id"] for t in avail_t],
                        format_func=lambda i: next(t["name"] for t in avail_t if t["id"] == i),
                        key="link_treatment",
                    )
                    if st.button("Link treatment"):
                        link_disease_treatment(did, tid)
                        st.rerun()

    with st.expander("Add disease", expanded=not diseases):
        crop_id = get_tomato_crop_id()
        if crop_id is None:
            st.warning("Tomato crop is not configured in the database.")
            st.stop()
        st.caption("New diseases are added to the tomato knowledge base.")
        name = st.text_input("Disease name", key="new_disease_name")
        desc = st.text_area("Description", key="new_disease_desc")
        template = st.text_area("Explanation template", key="new_disease_template")
        if st.button("Add disease", type="primary"):
            create_disease(crop_id, name, desc, template)
            st.success("Disease added. Link symptoms from the edit section.")
            st.rerun()
