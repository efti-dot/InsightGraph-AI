import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from app.services.run_service import start_run

st.title("InsightGraph AI")

with st.form("new_research"):
    project_name = st.text_input("Project Name")
    research_goal = st.text_area("Research Goal",height=120)
    submitted = st.form_submit_button("Analyze")

if submitted:
    if not research_goal.strip():
        st.warning("Please enter a research goal!")
    else:
        with st.spinner("Please wait some moment..."):
            result = start_run(
                project_id=project_name.strip() or "untitled-project",
                research_goal=research_goal.strip()
            )

        st.success(result.get("status", "Done"))
        st.subheader("Draft Report")
        st.markdown(result.get("draft_report", "No report generated."))