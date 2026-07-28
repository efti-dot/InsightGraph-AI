from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState

SYSTEM_PROMPT = """You are a professional business analyst who writes clear,
concise research report drafts. Structure your output with these sections:

## Executive Summary
## Market Overview
## Data Analysis
## Key Considerations
## Next Steps

Ground your writing in the findings you're given, and note when internal
documents, web findings, and data analysis agree or disagree. Where a
section has no supporting findings, say plainly what data would be needed
instead of inventing facts. Keep it under 450 words."""

def report_writer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    pdf_findings = state.get("pdf_findings", "")
    web_findings = state.get("web_findings", "")
    csv_analysis = state.get("csv_analysis", "")

    user_content = f"Research goal:\n{goal}"
    if pdf_findings:
        user_content += f"\n\nFindings from internal documents (PDFs):\n{pdf_findings}"
    if web_findings:
        user_content += f"\n\nFindings from web search:\n{web_findings}"
    if csv_analysis:
        user_content += f"\n\nFindings from data analysis (CSVs):\n{csv_analysis}"

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