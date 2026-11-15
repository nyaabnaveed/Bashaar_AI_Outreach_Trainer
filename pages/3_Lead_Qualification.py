import streamlit as st

from utils.lead_router import qualify_lead
from database.db import create_leads_table, save_lead
from utils.ui import (
    setup_page,
    page_header,
    section_title,
    card,
    text_block,
    info_grid,
    badge,
    notice,
    esc,
)

create_leads_table()

setup_page("Lead Qualification", active="leads")

page_header(
    "Module 03",
    "Lead Qualification",
    "Analyse incoming customer inquiries and identify the leads most "
    "likely to become customers.",
)


def category_indicator(category):
    """Shows Hot, Warm and Cold side by side with the active one highlighted."""
    kinds = {"Hot": "hot", "Warm": "warm", "Cold": "cold"}
    pills = ""
    for name, kind in kinds.items():
        if name == category:
            pills += str(badge(name, kind, True))
        else:
            pills += (
                '<span style="opacity:0.28;">'
                + str(badge(name, "neutral", True))
                + "</span>"
            )
    return (
        '<div class="bz-panel">'
        '<div class="bz-label">Lead category</div>'
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;">{pills}</div>'
        "</div>"
    )


# ------------------------------------------------------------------ Inquiry
section_title(
    "Incoming customer inquiry",
    "Paste the customer message exactly as it was received.",
)

with card():

    inquiry = st.text_area(
        "Enter customer message",
        placeholder="Example: Hi, I need an AI solution for my business. My budget is $1000 and I want to start within two weeks...",
        height=180
    )

    analyze = st.button("Analyze Lead", type="primary")

# ------------------------------------------------------------------ Results
if analyze:

    if not inquiry.strip():
        notice("Please enter a customer inquiry first.")

    else:
        with st.spinner("AI is analyzing the customer inquiry..."):

            try:
                result = qualify_lead(inquiry)

                save_lead(inquiry, result)

                notice("Lead analyzed and saved successfully.")

                section_title("Lead classification")

                col_category, col_urgency = st.columns([2, 1])

                with col_category:
                    st.markdown(
                        category_indicator(result["lead_category"]),
                        unsafe_allow_html=True,
                    )

                with col_urgency:
                    st.markdown(
                        '<div class="bz-panel">'
                        '<div class="bz-label">Urgency</div>'
                        f'<div class="bz-heading" style="margin-top:10px;">{esc(result["urgency"])}</div>'
                        "</div>",
                        unsafe_allow_html=True,
                    )

                section_title("Extracted lead information")

                info_grid([
                    ("Budget", result["budget"]),
                    ("Needs", result["needs"]),
                    ("Timeline", result["timeline"]),
                ])

                section_title("AI reasoning")
                text_block("Classification reasoning", result["reasoning"])

            except Exception as e:
                notice(f"Something went wrong: {e}", "error")