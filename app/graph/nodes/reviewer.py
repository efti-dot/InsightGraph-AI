from app.config import settings
from app.graph.state import ResearchState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

MAX_REVISIONS = 3


def reviewer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    draft_report = state.get("draft_report", "")
    merged_knowledge = state.get("merged_knowledge", "")
    revision_count = state.get("revision_count", 0)

    if revision_count >= MAX_REVISIONS:
        print(f"[reviewer] revision cap ({MAX_REVISIONS}) reached, approving as-is")
        return {
            "review_feedback": f"Approved after reaching the max of {MAX_REVISIONS} revision attempts.",
            "review_decision": "approve",
        }