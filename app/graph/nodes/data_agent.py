from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState

def data_agent_node(state: ResearchState) -> ResearchState:
    csv_paths = state.get("csv_paths", [])

    if not csv_paths:
        if not csv_paths:
            print("[data_agent] skipped (no files)")
            return {"csv_analysis": "No CSV files were uploaded for this project."}

    goal = state.get("research_goal", "")

    summaries = []
    