import app.path_setup  # noqa: F401

from app.ui.components.farmer_diagnosis import render_farmer_diagnosis
from app.ui.components.farmer_theme import inject_farmer_theme
from app.utils.auth import require_expert

require_expert()
inject_farmer_theme()
render_farmer_diagnosis(farmer_id=None, allow_farmer_select=True, key_prefix="admin")
