import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.consultation_repository import get_farmer_dashboard_stats
from app.services.consultation_service import ConsultationService
from app.ui.components.farmer_theme import inject_farmer_theme, render_page_header
from app.utils.auth import require_farmer

user = require_farmer()
inject_farmer_theme()

farmer_id = user.get("farmer_id")
if not farmer_id:
    st.warning("No farmer profile linked to this account.")
    st.stop()

render_page_header("Dashboard")

stats = get_farmer_dashboard_stats(farmer_id)
service = ConsultationService()
history = service.get_history(farmer_id=farmer_id, limit=10)

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.metric("Total Diagnoses", stats["total"])
with c2:
    with st.container(border=True):
        st.metric("This Month", stats["this_month"], delta=f"+{stats.get('this_week', 0)} this week")
with c3:
    with st.container(border=True):
        st.metric("Common Issue", stats["common_disease"])

st.subheader("Disease frequency")
if history:
    freq = pd.DataFrame(history).groupby("diagnosed_disease", dropna=True).size().reset_index(name="count")
    freq = freq[freq["diagnosed_disease"].notna()]
    if not freq.empty:
        st.bar_chart(freq.set_index("diagnosed_disease")["count"])
    else:
        st.info("No diagnosed diseases yet.")
else:
    st.info("No diagnoses yet.")

st.subheader("Recent Diagnoses")
if history:
    table = pd.DataFrame(
        [
            {
                "Date": row["consultation_date"].strftime("%b %d, %Y")
                if hasattr(row["consultation_date"], "strftime")
                else str(row["consultation_date"])[:10],
                "Disease": row["diagnosed_disease"] or "-",
                "Confidence": row.get("confidence_score") or 0,
                "Source": "Image" if row.get("source") == "IMAGE" else "Symptoms",
            }
            for row in history[:4]
        ]
    )
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Confidence": st.column_config.ProgressColumn(
                "Confidence", min_value=0, max_value=100, format="%d%%"
            )
        },
    )
else:
    st.info("No diagnoses yet. Use Diagnosis to run your first consultation.")
