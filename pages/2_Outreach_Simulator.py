import streamlit as st

from utils.outreach_coach import evaluate_outreach
from database.db import create_outreach_table, save_outreach_attempt
from utils.ui import (
    setup_page,
    page_header,
    section_title,
    card,
    score_card,
    text_block,
    notice,
    esc,
)

create_outreach_table()

setup_page("Outreach Simulator", active="outreach")

page_header(
    "Module 02",
    "Outreach Simulator",
    "Practise your outreach messages and receive instant AI feedback on "
    "hook, value proposition and call to action.",
)


def rating(score):
    """Short quality label shown under each score."""
    if score >= 8:
        return "Strong"
    if score >= 7:
        return "Solid"
    return "Needs improvement"


# ----------------------------------------------------------- Campaign setup
section_title("Campaign setup", "Enter your name and choose who you are writing to.")

with card():

    col_name, col_campaign = st.columns(2)

    with col_name:
        intern_name = st.text_input("Enter your name")

    with col_campaign:
        campaign = st.selectbox(
            "Choose your target audience",
            ["Retail Apparel", "Student AI Mentorship"]
        )

    if campaign == "Retail Apparel":
        notice(
            "Target: Retail clothing stores and apparel brands. "
            "Focus on their business challenges and how AI can help.",
            "info",
        )
    else:
        notice(
            "Target: Students interested in AI mentorship and learning opportunities.",
            "info",
        )

# --------------------------------------------------------- Outreach message
section_title("Your outreach message", "Write the message exactly as you would send it.")

with card():

    message = st.text_area(
        "Your Message",
        placeholder="Write your cold outreach message here...",
        height=180
    )

    evaluate = st.button("Evaluate Message", type="primary")

# ------------------------------------------------------------------ Results
if evaluate:

    if not intern_name.strip():
        notice("Please enter your name.")

    elif not message.strip():
        notice("Please write an outreach message first.")

    else:
        with st.spinner("AI Sales Coach is evaluating your message..."):

            try:
                result = evaluate_outreach(message, campaign)

                save_outreach_attempt(
                    intern_name,
                    campaign,
                    message,
                    result
                )

                notice("Your outreach message has been evaluated and saved.")

                section_title("AI evaluation results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    score_card(
                        "Hook Quality",
                        result["hook_score"],
                        note=rating(result["hook_score"]),
                    )

                with col2:
                    score_card(
                        "Value Proposition",
                        result["value_score"],
                        note=rating(result["value_score"]),
                    )

                with col3:
                    score_card(
                        "CTA Clarity",
                        result["cta_score"],
                        note=rating(result["cta_score"]),
                    )

                section_title("Feedback")
                text_block("Overall feedback", result["overall_feedback"])

                section_title("Improvement suggestions")

                if result["improvement_suggestions"]:
                    rows = ""
                    for index, suggestion in enumerate(
                        result["improvement_suggestions"], start=1
                    ):
                        border = "" if index == 1 else "border-top:1px solid #1B1C20;"
                        rows += (
                            f'<div class="bz-text" style="display:flex;gap:16px;'
                            f'padding:14px 0;{border}">'
                            f'<span style="color:#C9A24B;font-weight:600;'
                            f'letter-spacing:0.08em;flex:none;">{index:02d}</span>'
                            f"<span>{esc(suggestion)}</span></div>"
                        )
                    st.markdown(
                        '<div class="bz-panel" style="padding-top:8px;padding-bottom:8px;">'
                        + rows
                        + "</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    notice("Great work! No major improvements needed.")

                section_title(
                    "Improved outreach message",
                    "A rewritten version you can copy and send.",
                )

                st.text_area(
                    "Your improved version",
                    value=result["improved_version"],
                    height=180
                )

            except Exception as e:
                notice(f"Something went wrong: {e}", "error")