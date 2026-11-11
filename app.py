from database.db import create_table, save_intern
create_table()
import streamlit as st

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
        [
            "Technical",
            "Sales",
            "Graphic Design",
            "Content"
        ]
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
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    interests = st.text_area(
        "What type of work interests you?"
    )

    submit = st.form_submit_button("Submit Profile")


if submit:

    if name and email and skills:

        save_intern(
            name,
            email,
            education,
            background,
            skills,
            experience,
            interests
        )

        st.success("Intern profile saved successfully!")

        st.subheader("Your Profile")
        st.write("Name:", name)
        st.write("Email:", email)
        st.write("Background:", background)
        st.write("Skills:", ", ".join(skills))

    else:
        st.error("Please enter your name, email and at least one skill.")
