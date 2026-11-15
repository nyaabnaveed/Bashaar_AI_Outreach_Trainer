import streamlit as st

from database.db import get_interns, get_leads
from utils.ui import (
    setup_page,
    page_header,
    section_title,
    metric_card,
    module_card,
)

setup_page("Dashboard", active="dashboard")


def safe_rows(loader):
    """Read rows for the overview numbers. Returns None if the table does not exist yet."""
    try:
        return loader()
    except Exception:
        return None


interns = safe_rows(get_interns)
leads = safe_rows(get_leads)

page_header(
    "Overview",
    "Welcome to Bashaar AI",
    "Your AI-powered workspace for intern assessment, outreach training "
    "and lead management.",
)

# ---------------------------------------------------------------- Overview
section_title("Platform overview")

col1, col2, col3 = st.columns(3)

with col1:
    metric_card(
        "Interns assessed",
        len(interns) if interns is not None else "-",
        "Registered intern profiles",
    )

with col2:
    metric_card(
        "Leads qualified",
        len(leads) if leads is not None else "-",
        "Inquiries analysed by AI",
    )

with col3:
    hot_count = (
        sum(1 for lead in leads if "hot" in str(lead[2] or "").lower())
        if leads is not None
        else "-"
    )
    metric_card("Hot leads", hot_count, "Highest priority inquiries")

# ----------------------------------------------------------------- Modules
section_title("Modules", "Select a module to continue.")

row1_left, row1_right = st.columns(2)

with row1_left:
    module_card(
        "user",
        "Intern Skill Assessor",
        "Analyse intern backgrounds and receive AI-recommended roles "
        "based on skills and experience.",
        "pages/1_Intern_Assessor.py",
    )

with row1_right:
    module_card(
        "message",
        "Outreach Simulator",
        "Practise outreach messages and receive scored feedback on hook, "
        "value proposition and call to action.",
        "pages/2_Outreach_Simulator.py",
    )

row2_left, row2_right = st.columns(2)

with row2_left:
    module_card(
        "target",
        "Lead Qualification",
        "Classify customer inquiries as Hot, Warm or Cold and extract "
        "the key lead details.",
        "pages/3_Lead_Qualification.py",
    )

with row2_right:
    module_card(
        "clipboard",
        "Task Manager",
        "Match qualified leads with the most suitable interns and track "
        "every assignment.",
        "pages/4_Task_Manager.py",
    )