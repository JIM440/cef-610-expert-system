import app.path_setup  # noqa: F401

import pandas as pd
import streamlit as st

from app.repositories.consultation_repository import get_admin_dashboard_stats
from app.services.consultation_service import ConsultationService
from app.services.report_service import ReportService
from app.ui.components.farmer_theme import inject_farmer_theme, render_page_header
from app.utils.auth import require_admin

require_admin()
inject_farmer_theme()
render_page_header("Dashboard", "System overview.")

stats = get_admin_dashboard_stats()
service = ConsultationService()
report = ReportService()
history = service.get_history(limit=10)
disease_stats = report.disease_frequency()

row1 = st.columns(4)
metrics = [
    ("Total Farmers", stats["farmer_count"], None),
    ("Consultations", stats["total_consultations"], f"+{stats.get('this_week', 0)} this week"),
    ("Diseases", stats["disease_count"], None),
    ("Diagnoses", stats["total_diagnoses"], f"+{stats.get('this_month', 0)} this month"),
]
for col, (label, value, delta) in zip(row1, metrics):
    with col:
        with st.container(border=True):
            st.metric(label, value, delta=delta)

row2 = st.columns(4)
for col, (label, value) in zip(
    row2,
    [
        ("Symptoms", stats["symptom_count"]),
        ("Rules", stats["rule_count"]),
        ("Treatments", stats["treatment_count"]),
        ("Crops", stats["crop_count"]),
    ],
):
    with col:
        with st.container(border=True):
            st.metric(label, value)

st.subheader("Disease frequency")
if disease_stats:
    df_freq = pd.DataFrame(disease_stats)
    name_col = "disease_name" if "disease_name" in df_freq.columns else df_freq.columns[0]
    count_col = "count" if "count" in df_freq.columns else "cnt" if "cnt" in df_freq.columns else df_freq.columns[-1]
    st.bar_chart(df_freq.set_index(name_col)[count_col])
else:
    st.info("No diagnosed diseases yet.")

st.subheader("Recent consultations")
if history:
    table = pd.DataFrame(
        [
            {
                "Date": row["consultation_date"].strftime("%b %d, %Y")
                if hasattr(row["consultation_date"], "strftime")
                else str(row["consultation_date"])[:10],
                "Farmer": row.get("farmer_name") or "-",
                "Disease": row["diagnosed_disease"] or "-",
                "Confidence": row.get("confidence_score") or 0,
                "Source": "Image" if row.get("source") == "IMAGE" else "Symptoms",
            }
            for row in history[:6]
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
    st.info("No consultations yet.")
