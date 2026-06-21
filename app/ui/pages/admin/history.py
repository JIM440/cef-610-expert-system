import app.path_setup  # noqa: F401

from app.ui.components.consultation_history_page import render_consultation_history_page
from app.ui.components.farmer_theme import inject_farmer_theme
from app.utils.auth import require_admin

require_admin()
inject_farmer_theme()
render_consultation_history_page(allow_farmer_filter=True, page_title="History")
