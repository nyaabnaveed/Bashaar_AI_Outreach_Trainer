from datetime import datetime, timedelta
import streamlit as st

from database.db import (
    create_task_assignments_table,
    get_leads,
    get_interns,
    save_task_assignment,
    get_assignment_for_lead,
    get_assignment_history,
)
from utils.task_assigner import assign_best_intern
from utils.ui import (
    setup_page,
    page_header,
    section_title,
    card,
    text_block,
    info_grid,
    notice,
    esc,
)

create_task_assignments_table()

def format_pakistan_time(timestamp):
    if not timestamp:
        return "N/A"

    try:
        utc_time = datetime.strptime(
            str(timestamp),
            "%Y-%m-%d %H:%M:%S"
        )

        pakistan_time = utc_time + timedelta(hours=5)

        return pakistan_time.strftime("%Y-%m-%d %I:%M:%S %p")

    except (ValueError, TypeError):
        return str(timestamp)
setup_page("Task Manager", active="tasks")

page_header(
    "Module 04",
    "Task Manager",
    "Assign qualified leads to the most suitable interns and track "
    "assignment decisions and history.",
)

# -------------------------------------------------------------- Load data

try:
    leads = get_leads()
    interns = get_interns()
except Exception as e:
    leads = []
    interns = []
    notice(f"Unable to load records: {e}", "error")

if not leads:
    notice(
        "No qualified leads are available yet. Please qualify a lead first.",
        "info",
    )

elif not interns:
    notice(
        "No intern profiles are available. Please register interns first.",
        "info",
    )

else:

    # --------------------------------------------------------- Lead selection

    section_title(
        "Select a lead",
        "Choose a qualified lead to find its best intern match.",
    )

    lead_options = {
        lead[0]: (
            f"Lead #{lead[0]}  |  "
            f"{str(lead[1] or 'No needs description')[:65]}  |  "
            f"{lead[2] or 'Unclassified'}"
        )
        for lead in leads
    }

    selected_lead = st.selectbox(
        "Choose customer lead",
        options=list(lead_options.keys()),
        format_func=lambda lead_id: lead_options[lead_id],
    )

    recommendation_key = f"task_recommendation_{selected_lead}"

    # ------------------------------------------------------ Current assignment

    section_title("Current assignment")

    try:
        current = get_assignment_for_lead(selected_lead)
    except Exception:
        current = None

    if current:
        current_intern_id, current_name, current_score, current_reason, current_date = current

        with card():
            st.markdown(
                '<div class="bz-label">Currently assigned intern</div>'
                f'<div class="bz-heading" style="margin-top:8px;">'
                f'{esc(current_name)}</div>',
                unsafe_allow_html=True,
            )

            info_grid([
                ("Match score", f"{current_score}%"),
                ("Assigned on", format_pakistan_time(current_date)),
            ])

            text_block("Assignment reason", current_reason)

    else:
        notice("This lead has not been assigned to an intern yet.", "info")

    # ------------------------------------------------------ Find best intern

    section_title(
        "Intern recommendation",
        "Find the strongest match using intern skills, background and role.",
    )

    with card():
        if st.button("Find Best Intern", type="primary"):
            try:
                with st.spinner("Finding the most suitable intern..."):
                    result = assign_best_intern(selected_lead)

                st.session_state[recommendation_key] = result

            except Exception as e:
                st.session_state.pop(recommendation_key, None)
                notice(f"Unable to find a match: {e}", "error")

    result = st.session_state.get(recommendation_key)

    if result:

        if not result.get("matched"):
            notice(
                result.get(
                    "message",
                    "No suitable intern found. No assignment has been made.",
                ),
                "warning",
            )

        else:
            with card():
                st.markdown(
                    '<div class="bz-label">Recommended intern</div>'
                    f'<div class="bz-heading" style="margin-top:8px;">'
                    f'{esc(result["intern_name"])}</div>',
                    unsafe_allow_html=True,
                )

                st.metric(
                    "Match score",
                    f'{result["match_score"]}%',
                )

                text_block(
                    "Why this intern was selected",
                    result["assignment_reason"],
                )

                if current:
                    notice(
                        "Confirming this recommendation will create a new "
                        "assignment. The previous assignment will remain "
                        "in the history.",
                        "info",
                    )

                if st.button(
                    "Confirm Reassignment" if current else "Confirm Assignment",
                    type="primary",
                ):
                    try:
                        save_task_assignment(
                            selected_lead,
                            result["intern_id"],
                            result["match_score"],
                            result["assignment_reason"],
                        )

                        st.session_state.pop(recommendation_key, None)

                        notice(
                            "Intern assignment saved successfully.",
                            "success",
                        )

                        st.rerun()

                    except Exception as e:
                        notice(
                            f"Unable to save assignment: {e}",
                            "error",
                        )

    # ------------------------------------------------------ Assignment history

    section_title(
        "Assignment history",
        "Review previous assignments and reassignment decisions for this lead.",
    )

    try:
        history = get_assignment_history(selected_lead)
    except Exception:
        history = []

    if history:
        with card():
            for index, record in enumerate(history, start=1):
                intern_name, match_score, reason, status, created_at = record

                st.markdown(
                    f'<div class="bz-label">Assignment {index:02d}</div>'
                    f'<div class="bz-heading" style="margin-top:6px;">'
                    f'{esc(intern_name)}</div>',
                    unsafe_allow_html=True,
                )

                info_grid([
                    ("Match score", f"{match_score}%"),
                    ("Status", status),
                    ("Date", format_pakistan_time(created_at)),
                ])

                text_block("Assignment reason", reason)

                if index != len(history):
                    st.markdown(
                        '<div style="border-top:1px solid #26272B;'
                        'margin:20px 0;"></div>',
                        unsafe_allow_html=True,
                    )

    else:
        notice(
            "No assignment history is available for this lead yet.",
            "info",
        )
