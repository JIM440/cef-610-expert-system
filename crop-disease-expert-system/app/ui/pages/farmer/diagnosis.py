import app.path_setup  # noqa: F401

import streamlit as st

from app.ui.components.farmer_diagnosis import render_farmer_diagnosis
from app.ui.components.farmer_theme import inject_farmer_theme
from app.utils.auth import require_farmer

user = require_farmer()
inject_farmer_theme()
render_farmer_diagnosis(farmer_id=user.get("farmer_id"))
