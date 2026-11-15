"""
Bashaar AI - shared design system.

This file contains ONLY presentation code (CSS, sidebar, small HTML helpers).
It does not touch the database, Gemini or any business logic.

Every page uses it like this:

    from utils.ui import setup_page, page_header

    setup_page("Intern Skill Assessor", active="assessor")
    page_header("Module 01", "Intern Skill Assessor", "Short subtitle here.")
"""

import base64
import html as _html
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

import streamlit as st

# --------------------------------------------------------------------------
# Paths and navigation
# --------------------------------------------------------------------------
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

# key        -> used by setup_page(active=...)
# slug       -> last part of the page URL (Streamlit removes the "1_" prefix)
NAV = [
    {"key": "dashboard", "label": "Dashboard", "path": "app.py",
     "slug": None, "icon": "dashboard"},
    {"key": "assessor", "label": "Intern Skill Assessor",
     "path": "pages/1_Intern_Assessor.py", "slug": "Intern_Assessor",
     "icon": "user"},
    {"key": "outreach", "label": "Outreach Simulator",
     "path": "pages/2_Outreach_Simulator.py", "slug": "Outreach_Simulator",
     "icon": "message"},
    {"key": "leads", "label": "Lead Qualification",
     "path": "pages/3_Lead_Qualification.py", "slug": "Lead_Qualification",
     "icon": "target"},
    {"key": "tasks", "label": "Task Manager",
     "path": "pages/4_Task_Manager.py", "slug": "Task_Manager",
     "icon": "clipboard"},
]

# --------------------------------------------------------------------------
# Icons (simple line icons, drawn as inline SVG - no extra dependency)
# --------------------------------------------------------------------------
ICONS = {
    "dashboard": (
        '<rect x="3" y="3" width="7" height="7" rx="1"/>'
        '<rect x="14" y="3" width="7" height="7" rx="1"/>'
        '<rect x="14" y="14" width="7" height="7" rx="1"/>'
        '<rect x="3" y="14" width="7" height="7" rx="1"/>'
    ),
    "user": (
        '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/>'
        '<circle cx="12" cy="7" r="4"/>'
    ),
    "message": (
        '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/>'
        '<circle cx="12" cy="12" r="6"/>'
        '<circle cx="12" cy="12" r="2"/>'
    ),
    "clipboard": (
        '<rect x="8" y="2" width="8" height="4" rx="1"/>'
        '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>'
        '<path d="M12 11h4"/><path d="M12 16h4"/>'
        '<path d="M8 11h.01"/><path d="M8 16h.01"/>'
    ),
}


def _svg(name, size=20, stroke="currentColor", width=1.6):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'
    )


def _mask_url(name):
    """CSS url() version of an icon, used for the sidebar navigation icons."""
    return 'url("data:image/svg+xml;utf8,' + quote(_svg(name, 24, "black", 1.8)) + '")'


# --------------------------------------------------------------------------
# Safe HTML helpers
# --------------------------------------------------------------------------
class Safe(str):
    """Marks a string as ready-made HTML that must not be escaped again."""


def esc(value):
    """Escape text for safe use inside HTML. Keeps line breaks."""
    if isinstance(value, Safe):
        return str(value)
    if value is None:
        return ""
    text = _html.escape(str(value), quote=True)
    # "$" would be treated as math by Streamlit's markdown renderer.
    text = text.replace("$", "&#36;")
    return text.replace("\r\n", "\n").replace("\n", "<br>")


def _html_block(*parts):
    """Join HTML pieces into one line (blank lines would break Streamlit markdown)."""
    return "".join(parts)


def icon(name, size=22):
    return Safe(_svg(name, size))


@lru_cache(maxsize=1)
def _logo_b64():
    try:
        return base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")
    except OSError:
        return ""


def logo_html(max_width=190, align="center"):
    """Logo at its natural proportions (width is limited, height stays automatic)."""
    data = _logo_b64()
    margin = "0 auto" if align == "center" else "0"
    if not data:
        return Safe(
            '<div class="bz-wordmark">BASHAAR <span>AI</span></div>'
        )
    return Safe(
        f'<img class="bz-logo" alt="Bashaar AI" '
        f'style="max-width:{int(max_width)}px;margin:{margin};" '
        f'src="data:image/png;base64,{data}">'
    )


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

:root{
  --bg:#0A0A0B;
  --surface:#121214;
  --surface-2:#17181B;
  --border:#26272B;
  --border-strong:#33343A;
  --gold:#C9A24B;
  --gold-hover:#D8B45F;
  --text:#F5F5F5;
  --muted:#A1A1A6;
  --faint:#6B6B70;
  --danger:#C96B6B;
}

/* ---------- Base ---------- */
.stApp{background:var(--bg);color:var(--text);font-family:'Montserrat','Segoe UI',system-ui,sans-serif;}
.stApp p,.stApp li,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp h4,
.stApp input,.stApp textarea,.stApp button,.stApp td,.stApp th,
.stApp [data-baseweb="select"],.stApp [data-baseweb="tab"]{
  font-family:'Montserrat','Segoe UI',system-ui,sans-serif !important;
}
.stApp h1,.stApp h2,.stApp h3,.stApp h4{color:var(--text);font-weight:600;letter-spacing:-0.01em;}
.stApp hr{border-color:var(--border);}
.stApp a{color:var(--gold);}
.stApp [data-testid="stCaptionContainer"],.stApp small{color:var(--faint);}

[data-testid="stHeader"]{background:transparent;}
[data-testid="stDecoration"]{display:none;}
#MainMenu,footer{visibility:hidden;}
[data-testid="stAppDeployButton"],.stDeployButton{display:none;}
[data-testid="stMainBlockContainer"],.block-container{
  padding:3rem 3rem 4rem 3rem;max-width:1200px;
}

/* ---------- Scrollbars ---------- */
::-webkit-scrollbar{width:8px;height:8px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:#2A2B30;border-radius:8px;}
::-webkit-scrollbar-thumb:hover{background:#3A3B41;}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{background:#0E0E10;border-right:1px solid var(--border);}
[data-testid="stSidebarNav"]{display:none;}
[data-testid="stSidebarUserContent"]{padding-top:0.5rem;}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:0.2rem;}
.bz-logo{display:block;width:100%;height:auto;}
.bz-wordmark{text-align:center;font-weight:600;letter-spacing:0.3em;color:var(--text);font-size:18px;}
.bz-wordmark span{color:var(--gold);}
.bz-side-logo{padding:4px 8px 22px 8px;border-bottom:1px solid var(--border);margin-bottom:22px;}
.bz-nav-label{font-size:10.5px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;
  color:var(--gold);padding:0 12px 10px 12px;}
.bz-side-footer{margin-top:34px;padding:18px 12px 0 12px;border-top:1px solid var(--border);
  font-size:11px;line-height:1.7;color:var(--faint);letter-spacing:0.04em;}

/* Page links (main area): outlined button look */
.stApp a[data-testid="stPageLink-NavLink"]{
  display:flex;align-items:center;justify-content:center;gap:10px;
  border:1px solid var(--border-strong);border-radius:8px;
  padding:0.5rem 1rem;background:transparent;color:var(--text) !important;
  text-decoration:none;transition:border-color .15s ease,color .15s ease;
}
.stApp a[data-testid="stPageLink-NavLink"]:hover{border-color:var(--gold);color:var(--gold) !important;background:transparent;}
.stApp a[data-testid="stPageLink-NavLink"] p{font-size:13px;font-weight:600;letter-spacing:0.03em;color:inherit !important;margin:0;}

/* Page links (sidebar): flat navigation rows */
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]{
  justify-content:flex-start;gap:12px;border:none;border-radius:8px;
  padding:0.62rem 0.8rem;color:var(--muted) !important;background:transparent;
  position:relative;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"] p{font-size:13.5px;font-weight:500;letter-spacing:0.01em;}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]:hover{
  background:var(--surface-2);color:var(--text) !important;border:none;
}
section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]::before{
  content:"";width:18px;height:18px;flex:none;background-color:currentColor;
}

/* ---------- Page header ---------- */
.bz-header{padding-bottom:26px;margin-bottom:34px;border-bottom:1px solid var(--border);}
.bz-eyebrow{font-size:11px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;color:var(--gold);margin-bottom:12px;}
.bz-title{font-size:30px;font-weight:600;letter-spacing:-0.015em;color:var(--text);line-height:1.2;margin:0;}
.bz-subtitle{font-size:14.5px;line-height:1.7;color:var(--muted);margin-top:10px;max-width:720px;}

.bz-section{margin:34px 0 14px 0;}
.bz-section-title{font-size:15px;font-weight:600;color:var(--text);letter-spacing:0.01em;}
.bz-section-caption{font-size:13px;color:var(--faint);margin-top:4px;line-height:1.6;}

/* ---------- Cards ---------- */
div[data-testid="stVerticalBlockBorderWrapper"]:has(.bz-card-marker){
  background:var(--surface);border:1px solid var(--border) !important;border-radius:12px;
  transition:border-color .15s ease,background-color .15s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.bz-card-marker.bz-hover):hover{
  border-color:rgba(201,162,75,0.55) !important;background:var(--surface-2);
}
[data-testid="stElementContainer"]:has(.bz-card-marker),
.element-container:has(.bz-card-marker){display:none;}

.bz-panel{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:22px 24px;}
.bz-panel + .bz-panel{margin-top:14px;}
.bz-label{font-size:10.5px;font-weight:600;letter-spacing:0.16em;text-transform:uppercase;color:var(--faint);margin-bottom:8px;}
.bz-text{font-size:14.5px;line-height:1.75;color:#E6E6E8;}
.bz-heading{font-size:22px;font-weight:600;color:var(--text);letter-spacing:-0.01em;line-height:1.3;}

.bz-iconbox{width:42px;height:42px;border:1px solid var(--border-strong);border-radius:10px;
  display:flex;align-items:center;justify-content:center;color:var(--gold);margin-bottom:18px;}
.bz-card-title{font-size:17px;font-weight:600;color:var(--text);margin-bottom:8px;}
.bz-card-desc{font-size:13.5px;line-height:1.7;color:var(--muted);min-height:46px;margin-bottom:20px;}

/* ---------- Metrics ---------- */
.bz-metric{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:18px 22px;}
.bz-metric-value{font-size:30px;font-weight:600;color:var(--text);letter-spacing:-0.02em;line-height:1.1;margin-top:6px;}
.bz-metric-caption{font-size:12px;color:var(--faint);margin-top:8px;}

/* ---------- Score cards ---------- */
.bz-score{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:20px 22px;}
.bz-score-value{font-size:34px;font-weight:600;color:var(--gold);letter-spacing:-0.02em;line-height:1;margin-top:6px;}
.bz-score-value span{font-size:14px;font-weight:500;color:var(--faint);margin-left:4px;letter-spacing:0;}
.bz-bar{height:4px;background:#1F2024;border-radius:4px;margin-top:16px;overflow:hidden;}
.bz-bar-fill{height:100%;background:var(--gold);border-radius:4px;}
.bz-score-note{font-size:12.5px;color:var(--muted);margin-top:12px;line-height:1.6;}

/* ---------- Key / value grid ---------- */
.bz-kv{display:grid;grid-template-columns:repeat(var(--bz-cols,3),minmax(0,1fr));gap:1px;
  background:var(--border);border:1px solid var(--border);border-radius:12px;overflow:hidden;}
@media (max-width:900px){.bz-kv{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media (max-width:560px){.bz-kv{grid-template-columns:minmax(0,1fr);}}
.bz-kv-item{background:var(--surface);padding:16px 20px;}
.bz-kv-value{font-size:14.5px;color:var(--text);line-height:1.6;}

/* ---------- Badges ---------- */
.bz-badge{display:inline-flex;align-items:center;gap:8px;padding:5px 13px;border-radius:999px;
  font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;border:1px solid transparent;line-height:1.4;}
.bz-badge-lg{padding:9px 22px;font-size:13px;}
.bz-badge-hot{background:var(--gold);color:#0A0A0B;border-color:var(--gold);}
.bz-badge-warm{background:transparent;color:var(--gold);border-color:var(--gold);}
.bz-badge-cold{background:transparent;color:var(--muted);border-color:#4A4B52;}
.bz-badge-neutral{background:var(--surface-2);color:var(--muted);border-color:var(--border-strong);}
.bz-badge-gold{background:rgba(201,162,75,0.08);color:var(--gold);border-color:rgba(201,162,75,0.45);}

/* ---------- Notices ---------- */
.bz-notice{background:var(--surface);border:1px solid var(--border);border-left:3px solid var(--gold);
  border-radius:8px;padding:12px 16px;font-size:13.5px;line-height:1.6;color:#E6E6E8;margin:10px 0;}
.bz-notice-error{border-left-color:var(--danger);}
.bz-notice-info{border-left-color:#5A5B62;}

/* ---------- Tables ---------- */
.bz-table-wrap{border:1px solid var(--border);border-radius:12px;overflow:auto;background:var(--surface);}
.bz-table{width:100%;border-collapse:collapse;font-size:13.5px;}
.bz-table th{text-align:left;padding:13px 18px;font-size:10.5px;font-weight:600;letter-spacing:0.14em;
  text-transform:uppercase;color:var(--faint);border-bottom:1px solid var(--border);background:#0F0F11;white-space:nowrap;}
.bz-table td{padding:14px 18px;color:#E6E6E8;border-bottom:1px solid #1B1C20;vertical-align:top;line-height:1.6;}
.bz-table tr:last-child td{border-bottom:none;}
.bz-table tbody tr:hover td{background:#15161A;}
.bz-empty{padding:34px 20px;text-align:center;color:var(--faint);font-size:13.5px;}

/* ---------- Streamlit widgets ---------- */
[data-testid="stWidgetLabel"] p,.stApp label p{font-size:12.5px;font-weight:500;color:var(--muted);letter-spacing:0.02em;}

div[data-baseweb="input"],div[data-baseweb="textarea"],div[data-baseweb="select"] > div{
  background:var(--bg) !important;border:1px solid var(--border-strong) !important;border-radius:8px !important;
  transition:border-color .15s ease;
}
div[data-baseweb="input"]:focus-within,div[data-baseweb="textarea"]:focus-within,
div[data-baseweb="select"] > div:focus-within{
  border-color:var(--gold) !important;box-shadow:0 0 0 1px var(--gold) !important;
}
div[data-baseweb="base-input"]{background:transparent !important;}
.stApp input,.stApp textarea{color:var(--text) !important;font-size:14px !important;}
.stApp input::placeholder,.stApp textarea::placeholder{color:var(--faint) !important;}
div[data-baseweb="popover"] ul{background:var(--surface) !important;}
div[data-baseweb="popover"] li:hover{background:var(--surface-2) !important;}

[data-testid="stForm"]{
  background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:26px 26px 20px 26px;
}

/* Buttons */
.stButton > button,.stFormSubmitButton > button,.stDownloadButton > button{
  border-radius:8px;font-weight:600;font-size:13.5px;letter-spacing:0.03em;padding:0.58rem 1.4rem;
  transition:background-color .15s ease,border-color .15s ease,color .15s ease;
}
.stApp button p{color:inherit !important;font-size:13.5px;font-weight:600;}
button[kind="secondary"],button[data-testid="stBaseButton-secondary"],button[data-testid="stBaseButton-secondaryFormSubmit"]{
  background:transparent !important;color:var(--text) !important;border:1px solid var(--border-strong) !important;
}
button[kind="secondary"]:hover,button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondaryFormSubmit"]:hover{
  border-color:var(--gold) !important;color:var(--gold) !important;
}
button[kind="primary"],button[data-testid="stBaseButton-primary"],button[data-testid="stBaseButton-primaryFormSubmit"]{
  background:var(--gold) !important;color:#0A0A0B !important;border:1px solid var(--gold) !important;
}
button[kind="primary"]:hover,button[data-testid="stBaseButton-primary"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover{
  background:var(--gold-hover) !important;border-color:var(--gold-hover) !important;color:#0A0A0B !important;
}
button:disabled{opacity:0.45;}

/* Built-in alerts (st.success / st.warning / st.error / st.info) */
[data-testid="stAlert"]{
  background:var(--surface) !important;border:1px solid var(--border);border-left:3px solid var(--gold);
  border-radius:8px;color:var(--text);
}
[data-testid="stAlert"] [data-baseweb="notification"]{background:transparent !important;}
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]){border-left-color:var(--danger);}
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]){border-left-color:#5A5B62;}
[data-testid="stAlert"] p{color:#E6E6E8;font-size:13.5px;}

/* Other built-ins */
[data-testid="stExpander"] details{background:var(--surface);border:1px solid var(--border);border-radius:10px;}
[data-testid="stExpander"] summary p{font-size:13.5px;font-weight:600;color:var(--text);}
[data-testid="stDataFrame"]{border:1px solid var(--border);border-radius:10px;overflow:hidden;}
[data-testid="stMetric"]{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px 20px;}
[data-testid="stMetricLabel"] p{font-size:11px;letter-spacing:0.12em;text-transform:uppercase;color:var(--faint);}
[data-testid="stMetricValue"]{font-weight:600;}
.stTabs [data-baseweb="tab-list"]{border-bottom:1px solid var(--border);gap:6px;}
.stTabs [data-baseweb="tab"] p{font-size:13.5px;font-weight:600;}
"""


def _build_css(active):
    css = BASE_CSS

    sidebar_link = 'section[data-testid="stSidebar"] a[data-testid="stPageLink-NavLink"]'

    # Default icon for every sidebar link, then one specific icon per page.
    css += f'{sidebar_link}::before{{-webkit-mask:{_mask_url("dashboard")} center/contain no-repeat;' \
           f'mask:{_mask_url("dashboard")} center/contain no-repeat;}}\n'
    for item in NAV:
        if item["slug"]:
            sel = f'{sidebar_link}[href$="{item["slug"]}"]::before'
            url = _mask_url(item["icon"])
            css += f'{sel}{{-webkit-mask:{url} center/contain no-repeat;mask:{url} center/contain no-repeat;}}\n'

    # Highlight for the page that is currently open.
    active_style = (
        "{background:#17181B;color:#F5F5F5 !important;"
        "box-shadow:inset 2px 0 0 #C9A24B;border-radius:0 8px 8px 0;}"
    )
    css += f'{sidebar_link}[aria-current="page"]{active_style}\n'
    slugs = [i["slug"] for i in NAV if i["slug"]]
    if active == "dashboard":
        exclusions = "".join(f':not([href$="{s}"])' for s in slugs)
        css += f"{sidebar_link}{exclusions}{active_style}\n"
    else:
        for item in NAV:
            if item["key"] == active and item["slug"]:
                css += f'{sidebar_link}[href$="{item["slug"]}"]{active_style}\n'

    return "<style>" + css + "</style>"


# --------------------------------------------------------------------------
# Public API - page setup
# --------------------------------------------------------------------------
def _page_icon():
    try:
        from PIL import Image  # Pillow is already installed with Streamlit
        return Image.open(LOGO_PATH)
    except Exception:
        return None


def setup_page(title, active="dashboard"):
    """
    Call this FIRST on every page (before any other st.* command).
    Sets the page config, injects the theme and draws the sidebar.
    """
    st.set_page_config(
        page_title=f"{title} | Bashaar AI",
        page_icon=_page_icon(),
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_build_css(active), unsafe_allow_html=True)
    _render_sidebar()


def _render_sidebar():
    with st.sidebar:
        st.markdown(
            _html_block('<div class="bz-side-logo">', logo_html(180), "</div>"),
            unsafe_allow_html=True,
        )
        
        for item in NAV:
            st.page_link(item["path"], label=item["label"])
        st.markdown(
            '<div class="bz-side-footer">Bashaar AI<br>AI Outreach Trainer &amp; Lead Router</div>',
            unsafe_allow_html=True,
        )


# --------------------------------------------------------------------------
# Public API - layout components
# --------------------------------------------------------------------------
def page_header(eyebrow, title, subtitle=""):
    sub = f'<div class="bz-subtitle">{esc(subtitle)}</div>' if subtitle else ""
    st.markdown(
        _html_block(
            '<div class="bz-header">',
            f'<div class="bz-eyebrow">{esc(eyebrow)}</div>',
            f'<h1 class="bz-title">{esc(title)}</h1>',
            sub,
            "</div>",
        ),
        unsafe_allow_html=True,
    )


def section_title(title, caption=""):
    cap = f'<div class="bz-section-caption">{esc(caption)}</div>' if caption else ""
    st.markdown(
        _html_block(
            '<div class="bz-section">',
            f'<div class="bz-section-title">{esc(title)}</div>',
            cap,
            "</div>",
        ),
        unsafe_allow_html=True,
    )


@contextmanager
def card(hover=False):
    """A bordered card. Use:  with card(): ...  (do not nest cards)."""
    with st.container(border=True):
        cls = "bz-card-marker bz-hover" if hover else "bz-card-marker"
        st.markdown(f'<span class="{cls}"></span>', unsafe_allow_html=True)
        yield


def metric_card(label, value, caption=""):
    cap = f'<div class="bz-metric-caption">{esc(caption)}</div>' if caption else ""
    st.markdown(
        _html_block(
            '<div class="bz-metric">',
            f'<div class="bz-label" style="margin-bottom:0">{esc(label)}</div>',
            f'<div class="bz-metric-value">{esc(value)}</div>',
            cap,
            "</div>",
        ),
        unsafe_allow_html=True,
    )


def score_card(label, score, maximum=10, suffix="", note=""):
    """Score with a thin progress line. For percentages use maximum=100, suffix='%'."""
    try:
        number = float(score)
    except (TypeError, ValueError):
        number = 0.0
    pct = 0 if not maximum else max(0.0, min(100.0, number / float(maximum) * 100))
    shown = int(number) if number == int(number) else round(number, 1)
    unit = suffix if suffix else f"/{maximum}"
    note_html = f'<div class="bz-score-note">{esc(note)}</div>' if note else ""
    st.markdown(
        _html_block(
            '<div class="bz-score">',
            f'<div class="bz-label" style="margin-bottom:0">{esc(label)}</div>',
            f'<div class="bz-score-value">{shown}<span>{esc(unit)}</span></div>',
            f'<div class="bz-bar"><div class="bz-bar-fill" style="width:{pct:.0f}%"></div></div>',
            note_html,
            "</div>",
        ),
        unsafe_allow_html=True,
    )


def text_block(label, text):
    """A labelled block of readable text (feedback, improved message, assessment...)."""
    st.markdown(
        _html_block(
            '<div class="bz-panel">',
            f'<div class="bz-label">{esc(label)}</div>',
            f'<div class="bz-text">{esc(text) if text else "-"}</div>',
            "</div>",
        ),
        unsafe_allow_html=True,
    )


def info_grid(items):
    """
    items = [("Label", "Value"), ...] shown as a clean specification grid.
    The number of columns is chosen so the last row is always completely
    filled (for example 6 items -> 3 columns x 2 rows).
    """
    count = len(items)
    if count <= 4:
        columns = max(count, 1)
    elif count % 3 == 0:
        columns = 3
    elif count % 4 == 0:
        columns = 4
    else:
        columns = 3

    cells = []
    for label, value in items:
        shown = esc(value) if value not in (None, "") else "-"
        cells.append(
            _html_block(
                '<div class="bz-kv-item">',
                f'<div class="bz-label">{esc(label)}</div>',
                f'<div class="bz-kv-value">{shown}</div>',
                "</div>",
            )
        )

    # Fill any remaining cells in the last row so no grey gap shows.
    while cells and len(cells) % columns != 0:
        cells.append('<div class="bz-kv-item"></div>')

    st.markdown(
        f'<div class="bz-kv" style="--bz-cols:{columns}">' + "".join(cells) + "</div>",
        unsafe_allow_html=True,
    )


def badge(text, kind="neutral", large=False):
    """Returns badge HTML. kind: hot | warm | cold | gold | neutral."""
    size = " bz-badge-lg" if large else ""
    return Safe(f'<span class="bz-badge bz-badge-{kind}{size}">{esc(text)}</span>')


def status_badge(value, large=False):
    """Hot / Warm / Cold badge. Works even if the text has extra words around it."""
    text = str(value or "").strip()
    lowered = text.lower()
    if "hot" in lowered:
        return badge("Hot", "hot", large)
    if "warm" in lowered:
        return badge("Warm", "warm", large)
    if "cold" in lowered:
        return badge("Cold", "cold", large)
    return badge(text or "Unknown", "neutral", large)


def show_badge(badge_html):
    """Display a badge returned by badge() / status_badge()."""
    st.markdown(str(badge_html), unsafe_allow_html=True)


def notice(text, kind="gold"):
    """Slim message bar. kind: gold | info | error."""
    cls = {"gold": "", "info": " bz-notice-info", "error": " bz-notice-error"}.get(kind, "")
    st.markdown(f'<div class="bz-notice{cls}">{esc(text)}</div>', unsafe_allow_html=True)


def html_table(headers, rows, empty_text="No records yet."):
    """
    Styled table. rows = list of lists. Text is escaped automatically;
    pass badge(...) results to show badges inside cells.
    """
    if not rows:
        st.markdown(
            f'<div class="bz-table-wrap"><div class="bz-empty">{esc(empty_text)}</div></div>',
            unsafe_allow_html=True,
        )
        return
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(cell) if cell not in (None, '') else '-'}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    st.markdown(
        _html_block(
            '<div class="bz-table-wrap"><table class="bz-table">',
            f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody>",
            "</table></div>",
        ),
        unsafe_allow_html=True,
    )


def module_card(icon_name, title, description, page_path, button_label="Open module"):
    """Dashboard module card with an icon, text and a link button."""
    with card(hover=True):
        st.markdown(
            _html_block(
                f'<div class="bz-iconbox">{icon(icon_name, 22)}</div>',
                f'<div class="bz-card-title">{esc(title)}</div>',
                f'<div class="bz-card-desc">{esc(description)}</div>',
            ),
            unsafe_allow_html=True,
        )
        st.page_link(page_path, label=button_label)