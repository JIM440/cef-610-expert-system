import app.path_setup  # noqa: F401

from app.ui.components.image_recognition_page import render_image_recognition_page
from app.utils.auth import require_farmer

require_farmer()
render_image_recognition_page(allow_farmer_select=False)
