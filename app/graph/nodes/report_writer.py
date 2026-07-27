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

Since no supporting research has been gathered yet in this draft, be explicit
about what data would be needed to strengthen each section. Keep it under
300 words."""

def report_writer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    pdf_findings = state.get("pdf_findings", "")

    user_content = f"Research goal:\n{goal}"
    if pdf_findings:
        user_content += f"\n\nFindings from internal documents (PDFs):\n{pdf_findings}"

    llm = ChatOpenAI(
        model=settings.model_name,
        api_key=settings.openai_api_key,
        temperature=0.3,
    )

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_content),
        ]
    )

    state["draft_report"] = response.content
    state["status"] = "Report writer: draft complete"
    return state