from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState

SYSTEM_PROMPT = """You are a professional business analyst who writes clear,
concise research report drafts. Structure your output with these sections:

## Executive Summary
## Market Overview
## Data Analysis
## Visualizations
## Key Considerations
## Next Steps

Ground your writing in the merged findings you're given. If conflicting
information between sources is noted, mention it explicitly (e.g. "sources
differ on the exact growth rate") rather than presenting one figure as
certain. In the Visualizations section, briefly describe what each named
chart shows and why it's relevant — don't restate the raw numbers, those
belong in Data Analysis. Where a section has no supporting findings, say
plainly what data would be needed instead of inventing facts. Keep it
under 500 words."""

def report_writer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    merged_knowledge = state.get("merged_knowledge", "")
    conflicts = state.get("conflicts", "")
    charts = state.get("charts", [])
    review_feedback = state.get("review_feedback", "")

    user_content = f"Research goal:\n{goal}\n\nMerged findings:\n{merged_knowledge}"

    if conflicts and "no conflicts" not in conflicts.lower():
        user_content += f"\n\nConflicts flagged by fact checker:\n{conflicts}"

    if charts:
        chart_titles = [c.get("title", "Untitled chart") for c in charts]
        user_content += f"\n\nCharts generated for this report (reference these by name in Visualizations, don't invent new data): {', '.join(chart_titles)}"
    else:
        user_content += "\n\nNo charts were generated (no CSV data was provided)."

    if review_feedback:
        user_content += (
            f"\n\nA previous draft was reviewed and needs revision. "
            f"Address this feedback directly:\n{review_feedback}"
        )

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