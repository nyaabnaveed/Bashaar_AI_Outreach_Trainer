import streamlit as st
from utils.lead_router import qualify_lead
from database.db import create_leads_table, save_lead

st.set_page_config(
    page_title="Lead Qualification | Bashaar AI",
    page_icon="🎯",
    layout="wide"
)

create_leads_table()

st.title("🎯 AI Lead Qualification")
st.write("Analyze incoming inquiries and identify potential customers.")

st.divider()

st.subheader("📩 Incoming Customer Inquiry")

inquiry = st.text_area(
    "Enter customer message",
    placeholder="Example: Hi, I need an AI solution for my business. My budget is $1000 and I want to start within two weeks...",
    height=180
)

if st.button("🔍 Analyze Lead", type="primary"):

    if not inquiry.strip():
        st.warning("Please enter a customer inquiry first.")

    else:
        with st.spinner("AI is analyzing the customer inquiry..."):

            try:
                result = qualify_lead(inquiry)

                save_lead(inquiry, result)

                st.success("Lead analyzed and saved successfully!")

                st.divider()
                st.header("📊 Lead Analysis Results")

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Customer Information")
                    st.write("**Budget:**", result["budget"])
                    st.write("**Needs:**", result["needs"])
                    st.write("**Timeline:**", result["timeline"])

                with col2:
                    st.subheader("Lead Classification")

                    st.metric("Urgency", result["urgency"])

                    category = result["lead_category"]

                    if category == "Hot":
                        st.error(f"🔥 {category} Lead")
                    elif category == "Warm":
                        st.warning(f"🟡 {category} Lead")
                    else:
                        st.info(f"🔵 {category} Lead")

                st.subheader("💡 AI Reasoning")
                st.write(result["reasoning"])

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()

st.caption("Bashaar AI | AI Outreach Trainer & Lead Router")