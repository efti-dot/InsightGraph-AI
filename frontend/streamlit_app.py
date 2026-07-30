import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from app.services.run_service import start_run
import plotly.io as pio
from app.services.export_service import export_all

st.title("InsightGraph AI")

with st.form("new_research"):
    project_name = st.text_input("Project Name")
    research_goal = st.text_area("Research Goal",height=120)
    uploaded_pdfs = st.file_uploader(
        "Upload PDFs (Optional)", type=["pdf"], accept_multiple_files=True
    )
    uploaded_csvs = st.file_uploader(
        "Upload CSVs (optional)", type=["csv"], accept_multiple_files=True
    )
    submitted = st.form_submit_button("Analyze")

if submitted:
    if not research_goal.strip():
        st.warning("Please enter a research goal.")
    else:
        project_id = project_name.strip() or "untitled-project"

        pdf_paths: list[str] = []
        csv_paths: list[str] = []
        upload_dir = os.path.join("storage", "uploads", project_id)

        if uploaded_pdfs or uploaded_csvs:
            os.makedirs(upload_dir, exist_ok=True)

        for f in uploaded_pdfs or []:
            path = os.path.join(upload_dir, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            pdf_paths.append(path)

        for f in uploaded_csvs or []:
            path = os.path.join(upload_dir, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            csv_paths.append(path)

        with st.spinner("Running agent graph..."):
            result = start_run(
                project_id=project_id,
                research_goal=research_goal.strip(),
                pdf_paths=pdf_paths,
                csv_paths=csv_paths,
            )

        with st.spinner("Preparing downloads..."):
            exported = export_all(
                project_id=project_id,
                draft_report=result.get("draft_report", ""),
                charts=result.get("charts", []),
            )

        st.session_state.result = result
        st.session_state.project_id = project_id
        st.session_state.exported = exported

if st.session_state.get("result"):
    result = st.session_state.get("result")
    exported = st.session_state.get("exported")

    st.success(result.get("status", "Done"))

    with st.expander("Raw agent findings (before merging)"):
        if result.get("pdf_findings"):
            st.markdown("**PDF Findings**")
            st.markdown(result["pdf_findings"])
        if result.get("web_findings"):
            st.markdown("**Web Research Findings**")
            st.markdown(result["web_findings"])
        if result.get("csv_analysis"):
            st.markdown("**Data Analysis Findings**")
            st.markdown(result["csv_analysis"])

    if result.get("merged_knowledge"):
        st.subheader("Merged Knowledge")
        st.markdown(result["merged_knowledge"])

    conflicts = result.get("conflicts", "")
    if conflicts and "no conflicts" not in conflicts.lower():
        st.subheader("Conflicts Flagged")
        st.warning(conflicts)

    charts = result.get("charts", [])
    if charts:
        st.subheader("Visualizations")
        for chart in charts:
            fig = pio.from_json(chart["figure_json"])
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Draft Report")
    st.markdown(result.get("draft_report", "No report generated."))

    review_decision = result.get("review_decision", "")
    revision_count = result.get("revision_count", 0)
    if review_decision:
        label = "Approved by reviewer" if review_decision == "approve" else "Sent back for revision"
        st.caption(f"{label} · {revision_count} revision round(s)")
        with st.expander("Reviewer feedback"):
            st.markdown(result.get("review_feedback", ""))

    st.subheader("Download Report")

    if exported.get("warning"):
        st.warning(exported["warning"])

    col1, col2, col3 = st.columns(3)
    with col1:
        with open(exported["markdown"], "rb") as f:
            st.download_button("Markdown (.md)", f, file_name="report.md", use_container_width=True)
    with col2:
        with open(exported["docx"], "rb") as f:
            st.download_button(
                "Word (.docx)",
                f,
                file_name="report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
    with col3:
        with open(exported["pdf"], "rb") as f:
            st.download_button(
                "PDF (.pdf)", f, file_name="report.pdf", mime="application/pdf", use_container_width=True
            )

    