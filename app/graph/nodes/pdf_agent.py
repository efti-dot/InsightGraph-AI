from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.graph.state import ResearchState

def pdf_agent_node(state: ResearchState) -> ResearchState:
    project_id = state.get("project_id", "default")
    goal = state.get("research_goal", "")
    uploaded_files = state.get("uploaded_files", [])

    if not uploaded_files:
        state["pdf_findings"] = "No PDFs were uploaded for this project."
        state["status"] = "PDF agent: skipped (no files)"
        return state

    