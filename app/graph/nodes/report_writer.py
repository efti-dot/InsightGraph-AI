from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState

SYSTEM_PROMPT = """You are a professional business analyst who writes clear,
concise research report drafts. Structure your output with these sections:

## Executive Summary
## Market Overview
## Key Considerations
## Next Steps
Keep it under 300 words.
"""

def report_writer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")

    llm = ChatOpenAI(
        model=settings.model_name,
        api_key=settings.openai_api_key,
        temperature=0.3,
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Research goal:\n{goal}"),
        ]
    )

    state["draft_report"] = response.content
    state["status"] = "Report writer: draft complete"
    return state