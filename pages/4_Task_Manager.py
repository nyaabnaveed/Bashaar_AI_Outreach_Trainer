
import streamlit as st

from database.db import (
    create_task_assignments_table,
    get_leads,
    get_interns,
    save_task_assignment,
    get_assignment_for_lead,
    get_assignment_history
)

from utils.task_assigner import assign_best_intern


st.set_page_config(
    page_title="Task Manager | Bashaar AI",
    page_icon="📋",
    layout="wide"
)

create_task_assignments_table()

st.title("📋 AI Task Manager")
st.write(
    "Match incoming leads with suitable interns "
    "and manage task assignments."
)

st.divider()

st.subheader("🎯 Lead Assignment")

leads = get_leads()
interns = get_interns()

if not leads:
    st.info("No leads available. Add a lead through Lead Qualification first.")

elif not interns:
    st.warning("No intern profiles available. Register an intern first.")

else:

    lead_options = {
        f"Lead #{lead[0]} - {lead[1]} ({lead[2]})": lead[0]
        for lead in leads
    }

    selected_lead = st.selectbox(
        "Select a lead",
        options=list(lead_options.keys())
    )

    lead_id = lead_options[selected_lead]

    current_assignment = get_assignment_for_lead(lead_id)

    if current_assignment:

        st.success("This lead already has an assignment.")

        st.subheader("📌 Current Assignment")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Assigned Intern:**", current_assignment[1])
            st.write("**Match Score:**", f"{current_assignment[2]}%")

        with col2:
            st.write("**Assigned On:**", current_assignment[4])

        st.write("**Assignment Reason:**")
        st.write(current_assignment[3])

        st.info(
            "You can find a new intern below. "
            "The previous assignment will remain in history."
        )

    else:
        st.info("This lead has not been assigned yet.")

    if st.button(
        "🔄 Find Best-Matched Intern",
        type="primary"
    ):

        try:
            result = assign_best_intern(lead_id)

            st.session_state["assignment_result"] = result
            st.session_state["assignment_lead_id"] = lead_id

        except Exception as e:
            st.error(f"Matching failed: {e}")

    result = st.session_state.get("assignment_result")

    if (
        result
        and st.session_state.get("assignment_lead_id") == lead_id
    ):

        st.divider()
        st.subheader("🤖 AI Matching Recommendation")

        if not result["matched"]:

            st.warning(result["message"])

        else:

            st.success("Suitable intern found!")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Recommended Intern",
                    result["intern_name"]
                )

            with col2:
                st.metric(
                    "Match Score",
                    f"{result['match_score']}%"
                )

            st.write("**Why this intern?**")
            st.write(result["assignment_reason"])

            button_label = (
                "🔄 Confirm Reassignment"
                if current_assignment
                else "✅ Confirm Assignment"
            )

            if st.button(button_label):

                try:
                    save_task_assignment(
                        lead_id,
                        result["intern_id"],
                        result["match_score"],
                        result["assignment_reason"]
                    )

                    st.session_state.pop("assignment_result", None)
                    st.session_state.pop("assignment_lead_id", None)

                    st.success("Assignment saved successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Could not save assignment: {e}")
st.divider()

st.subheader("📜 Assignment History")

if leads and interns:

    history = get_assignment_history(lead_id)

    if history:

        for index, record in enumerate(history, start=1):

            st.write(f"**Assignment #{index}**")

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Intern:**", record[0])
                st.write("**Match Score:**", f"{record[1]}%")

            with col2:
                st.write("**Status:**", record[3])
                st.write("**Assigned On:**", record[4])

            st.write("**Reason:**", record[2])

            st.divider()

    else:
        st.info("No assignment history available for this lead.")

st.divider()

st.caption("Bashaar AI | AI Outreach Trainer & Lead Router")
