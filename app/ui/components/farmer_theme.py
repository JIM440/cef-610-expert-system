import streamlit as st

from app.ui.theme import inject_theme, render_page_header
from app.utils.auth import current_user


def inject_farmer_theme() -> None:
    if current_user():
        inject_theme()
