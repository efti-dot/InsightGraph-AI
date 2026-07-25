import streamlit as st

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
            st.success("this is the result.")