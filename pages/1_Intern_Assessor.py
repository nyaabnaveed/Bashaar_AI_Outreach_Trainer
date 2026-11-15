import streamlit as st

from database.db import create_table, save_intern
from utils.role_mapper import assign_role
from utils.ui import (
    setup_page,
    page_header,
    section_title,
    text_block,
    info_grid,
    notice,
    esc,
)

create_table()

setup_page("Intern Skill Assessor", active="assessor")

page_header(
    "Module 01",
    "Intern Skill Assessor",
    "Complete the registration below to receive a personalised role "
    "recommendation based on your skills, background and interests.",
)

# ------------------------------------------------------------ Registration
section_title(
    "Intern registration",
    "Your details are analysed by AI to assign the most suitable role.",
)

with st.form("intern_form"):

    col_name, col_email = st.columns(2)
    with col_name:
        name = st.text_input("Full Name")
    with col_email:
        email = st.text_input("Email Address")

    col_education, col_background = st.columns(2)
    with col_education:
        education = st.text_input("Education")
    with col_background:
        background = st.selectbox(
            "Select Your Background",
            ["Technical", "Sales", "Graphic Design", "Content"]
        )

    skills = st.multiselect(
        "Select Your Skills",
        [
            "Python",
            "Java",
            "AI Automation",
            "Make.com",
            "Communication",
            "Sales",
            "Graphic Design",
            "Content Writing",
            "Social Media Marketing"
        ]
    )

    experience = st.selectbox(
        "Experience Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

    interests = st.text_area(
        "What type of work interests you?"
    )

    submit = st.form_submit_button("Submit Profile", type="primary")


# ------------------------------------------------------------------ Result
if submit:

    if name.strip() and email.strip() and skills:

        try:
            with st.spinner("AI is analyzing your profile..."):

                result = assign_role(
                    name,
                    education,
                    background,
                    skills,
                    experience,
                    interests
                )

                assigned_role = result["assigned_role"]
                assessment = result["assessment"]

                save_intern(
                    name,
                    email,
                    education,
                    background,
                    skills,
                    experience,
                    interests,
                    assigned_role,
                    assessment
                )

            notice("Your profile has been assessed and saved successfully.")

            section_title("Role assignment")

            col_role, col_assessment = st.columns([1, 2])

            with col_role:
                st.markdown(
                    '<div class="bz-panel">'
                    '<div class="bz-label">Recommended role</div>'
                    f'<div class="bz-heading">{esc(assigned_role)}</div>'
                    "</div>",
                    unsafe_allow_html=True,
                )

            with col_assessment:
                text_block("Why this role", assessment)

            section_title("Profile summary")

            info_grid([
                ("Name", name),
                ("Email", email),
                ("Education", education),
                ("Background", background),
                ("Experience level", experience),
                ("Skills", ", ".join(skills)),
            ])

        except Exception as e:
            notice(f"Something went wrong: {e}", "error")

    else:
        notice("Please enter your name, email and at least one skill.", "error")