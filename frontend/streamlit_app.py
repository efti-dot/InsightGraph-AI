import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from app.services.run_service import start_run

st.title("InsightGraph AI")

with st.form("new_research"):
    project_name = st.text_input("Project Name")
    research_goal = st.text_area("Research Goal",height=120)
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs (Optional)", type=["pdf"], accept_multiple_files=True
    )
    submitted = st.form_submit_button("Analyze")

if submitted:
    if not research_goal.strip():
        st.warning("Please enter a research goal!")
    else:
        project_id=project_name.strip() or "untitled-project"
        pdf_paths: list[str] = []
        if uploaded_pdfs:
            upload_dir = os.path.join("storage", "uploads", project_id)
            os.makedirs(upload_dir, exist_ok=True)
            for f in uploaded_pdfs:
                path = os.path.join(upload_dir, f.name)
                with open(path, "wb") as out:
                    out.write(f.getbuffer())
                pdf_paths.append(path)
        with st.spinner("Please wait some moment..."):
            result = start_run(
                project_id=project_id,
                research_goal=research_goal.strip(),
                pdf_paths=pdf_paths,
            )

        st.success(result.get("status", "Done"))

        if result.get("pdf_findings"):
            st.subheader("PDF Findings")
            st.markdown(result["pdf_findings"])

        st.subheader("Draft Report")
        st.markdown(result.get("draft_report", "No report generated."))