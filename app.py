
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

st.divider()

st.caption("Bashaar AI | AI Outreach Trainer & Lead Router")
