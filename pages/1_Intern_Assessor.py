
import streamlit as st

from database.db import create_table, save_intern
from utils.role_mapper import assign_role

create_table()

st.set_page_config(
    page_title="Bashaar AI",
    page_icon="🤖",
    layout="wide"
)

st.title("Bashaar AI")
st.subheader("AI Outreach Trainer & Lead Router")

st.divider()

st.header("AI Intern Skill Assessor")
st.write("Complete the form to get your personalized role recommendation.")

with st.form("intern_form"):

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    education = st.text_input("Education")

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

    submit = st.form_submit_button("Submit Profile")


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

            st.success("Your profile has been assessed successfully!")

            st.divider()

            st.subheader("Your AI Recommended Role")
            st.success(assigned_role)

            st.write("**Why this role?**")
            st.write(assessment)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    else:
        st.error("Please enter your name, email and at least one skill.")
