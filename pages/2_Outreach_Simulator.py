import streamlit as st
from utils.outreach_coach import evaluate_outreach
from database.db import create_outreach_table, save_outreach_attempt

st.set_page_config(
    page_title="Outreach Simulator | Bashaar AI",
    page_icon="💬",
    layout="wide"
)

create_outreach_table()

st.title("💬 AI Outreach Simulator")
st.write("Practice your outreach messages and get instant AI feedback.")

st.divider()

# Intern Details
st.subheader("👤 Intern Details")

intern_name = st.text_input("Enter your name")

# Campaign Selection
st.subheader("🎯 Select Campaign")

campaign = st.selectbox(
    "Choose your target audience",
    ["Retail Apparel", "Student AI Mentorship"]
)

if campaign == "Retail Apparel":
    st.info(
        "Target: Retail clothing stores and apparel brands. "
        "Focus on their business challenges and how AI can help."
    )
else:
    st.info(
        "Target: Students interested in AI mentorship and learning opportunities."
    )

# Outreach Message
st.subheader("✉️ Write Your Outreach Message")

message = st.text_area(
    "Your Message",
    placeholder="Write your cold outreach message here...",
    height=180
)

# Evaluate Button
if st.button("🚀 Evaluate My Message", type="primary"):

    if not intern_name.strip():
        st.warning("Please enter your name.")

    elif not message.strip():
        st.warning("Please write an outreach message first.")

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

                st.success("Your outreach message has been evaluated and saved!")

                st.divider()
                st.header("📊 AI Evaluation Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Hook Quality", f"{result['hook_score']}/10")

                with col2:
                    st.metric("Value Proposition", f"{result['value_score']}/10")

                with col3:
                    st.metric("CTA Clarity", f"{result['cta_score']}/10")

                st.subheader("📝 Overall Feedback")
                st.write(result["overall_feedback"])

                st.subheader("💡 Improvement Suggestions")

                if result["improvement_suggestions"]:
                    for suggestion in result["improvement_suggestions"]:
                        st.write(f"• {suggestion}")
                else:
                    st.write("Great work! No major improvements needed.")

                st.subheader("✨ Improved Outreach Message")
                st.text_area(
                    "Your improved version",
                    value=result["improved_version"],
                    height=180
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()

st.caption("Bashaar AI | AI Outreach Trainer & Lead Router")