import app.path_setup  # noqa: F401

import streamlit as st

from app.ui.components.consultation_history_page import render_consultation_history_page
from app.ui.components.farmer_theme import inject_farmer_theme
from app.utils.auth import require_farmer

user = require_farmer()
inject_farmer_theme()

farmer_id = user.get("farmer_id")
if not farmer_id:
    st.warning("No farmer profile linked to this account.")
    st.stop()

render_consultation_history_page(farmer_id=farmer_id, page_title="My History")
