
import streamlit as st

st.set_page_config(
    page_title="Bashaar AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Bashaar AI")
st.subheader("AI Outreach Trainer & Lead Router")

st.divider()

st.header("Welcome to Bashaar AI!")
st.write(
    "Your AI-powered workspace for intern assessment, "
    "outreach training and lead management."
)

st.subheader("Application Modules")

# First Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("👩‍💻 Intern Skill Assessor")
    st.write(
        "Analyze intern skills and get AI-powered role recommendations."
    )
    st.page_link(
        "pages/1_Intern_Assessor.py",
        label="Open Intern Assessor",
        icon="👩‍💻"
    )

with col2:
    st.subheader("💬 Outreach Simulator")
    st.write(
        "Practice outreach messages and receive AI feedback."
    )
    st.page_link(
        "pages/2_Outreach_Simulator.py",
        label="Open Outreach Simulator",
        icon="💬"
    )

# Second Row
col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 AI Lead Qualification")
    st.write(
        "Analyze customer inquiries and classify leads as Hot, Warm or Cold."
    )
    st.page_link(
        "pages/3_Lead_Qualification.py",
        label="Open Lead Qualification",
        icon="🎯"
    )

with col4:
    st.subheader("📋 AI Task Manager")
    st.write(
        "Automatically match incoming leads with the most suitable interns."
    )
    st.page_link(
        "pages/4_Task_Manager.py",
        label="Open Task Manager",
        icon="📋"
    )

st.divider()

st.caption("Bashaar AI | AI Outreach Trainer & Lead Router")
