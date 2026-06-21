import html

import streamlit as st


PALETTE = {
    "forest": "#1B4332",
    "forest_2": "#153528",
    "leaf": "#2D6A4F",
    "success": "#40916C",
    "amber": "#E07A3E",
    "warning": "#B85C38",
    "danger": "#B45353",
    "bg": "#FAFAF7",
    "surface": "#FFFFFF",
    "line": "#DDE5DA",
    "text": "#18251F",
    "muted": "#66736B",
}


def configure_page() -> None:
    st.set_page_config(
        page_title="Tomato Disease Expert System",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_theme() -> None:
    st.markdown(
        f"""
        <style>
            :root {{
                --forest: {PALETTE["forest"]};
                --leaf: {PALETTE["leaf"]};
                --amber: {PALETTE["amber"]};
                --danger: {PALETTE["danger"]};
                --bg: {PALETTE["bg"]};
                --surface: {PALETTE["surface"]};
                --line: {PALETTE["line"]};
                --text: {PALETTE["text"]};
                --muted: {PALETTE["muted"]};
            }}
            .stApp {{ background: var(--bg); color: var(--text); }}
            .main .block-container {{ padding-top: 1.4rem; max-width: 1220px; }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, {PALETTE["forest"]} 0%, {PALETTE["forest_2"]} 100%);
                border-right: 1px solid rgba(255,255,255,0.08);
            }}
            [data-testid="stSidebar"] * {{ color: #F7FBF8 !important; }}
            [data-testid="stSidebar"] [data-testid="stSidebarNav"] {{
                padding-top: 0.4rem;
            }}
            [data-testid="stSidebar"] .stButton button {{
                background: rgba(255,255,255,0.1) !important;
                border: 1px solid rgba(255,255,255,0.22) !important;
                color: #fff !important;
                border-radius: 8px !important;
            }}
            h1, h2, h3 {{ color: var(--text); letter-spacing: 0; }}
            .stButton > button, button[data-testid^="stBaseButton"] {{
                border-radius: 8px !important;
                font-weight: 700 !important;
            }}
            .stButton button[kind="primary"], button[data-testid="stBaseButton-primary"] {{
                background: var(--amber) !important;
                border: 1px solid var(--amber) !important;
                color: #fff !important;
            }}
            div[data-testid="stDataFrame"] {{
                border: 1px solid var(--line);
                border-radius: 8px;
                overflow: hidden;
                background: var(--surface);
            }}
            .app-card, .result-card {{
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 1rem;
                box-shadow: 0 10px 24px rgba(27,67,50,0.06);
            }}
            .stat-card {{
                background: var(--surface);
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 1rem 1.1rem;
                min-height: 96px;
                box-shadow: 0 8px 20px rgba(27,67,50,0.05);
            }}
            .stat-card .value {{ font-size: 1.6rem; font-weight: 800; color: var(--forest); }}
            .stat-card .label {{ color: var(--muted); font-size: 0.82rem; margin-top: 0.25rem; }}
            .confidence-chip {{
                display: inline-block;
                min-width: 78px;
                text-align: center;
                border-radius: 999px;
                padding: 0.18rem 0.55rem;
                font-size: 0.78rem;
                font-weight: 800;
            }}
            .confidence-high {{ background:#DDEFE5; color:#1B5E3A; }}
            .confidence-mid {{ background:#FFF1DA; color:#9A4F12; }}
            .confidence-low {{ background:#F8DEDE; color:#8E3434; }}
            .status-chip {{
                display:inline-block;
                border-radius:999px;
                padding:0.16rem 0.5rem;
                font-size:0.76rem;
                font-weight:700;
                background:#EAF2ED;
                color:#1B4332;
            }}
            .disease-name {{ font-size: 1.9rem; font-weight: 800; color: var(--forest); }}
            .stepper {{ display:flex; align-items:center; gap:1rem; margin:1rem 0 1.4rem; }}
            .step {{ display:flex; align-items:center; gap:0.45rem; font-weight:700; color:#87928B; }}
            .step.active, .step.done {{ color: var(--leaf); }}
            .step-num {{
                width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center;
                border:2px solid #C9D4CD; background:#fff; font-size:0.8rem;
            }}
            .step.active .step-num, .step.done .step-num {{ border-color:var(--leaf); background:var(--leaf); color:#fff; }}
            .sidebar-user {{
                padding: 0.85rem;
                border: 1px solid rgba(255,255,255,0.18);
                border-radius: 8px;
                background: rgba(255,255,255,0.08);
                margin-bottom: 0.8rem;
            }}
            .sidebar-user .name {{ font-size: 0.98rem; font-weight: 800; }}
            .sidebar-user .role {{ font-size: 0.78rem; opacity: 0.82; margin-top: 0.15rem; }}
            .sidebar-section {{
                margin: 0.85rem 0 0.35rem;
                padding-top: 0.75rem;
                border-top: 1px solid rgba(255,255,255,0.16);
                font-size: 0.76rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0;
                opacity: 0.76;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str = "") -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)


def confidence_label(value: int | float | None) -> str:
    if value is None:
        return "—"
    value = int(value)
    tier = "high" if value > 80 else "mid" if value >= 60 else "low"
    return f"{value}% ({tier})"


def confidence_chip(value: int | float | None) -> str:
    if value is None:
        return '<span class="confidence-chip confidence-low">—</span>'
    value = int(value)
    tier = "high" if value > 80 else "mid" if value >= 60 else "low"
    return f'<span class="confidence-chip confidence-{tier}">{value}%</span>'


def escape(value: object) -> str:
    return html.escape("" if value is None else str(value))
