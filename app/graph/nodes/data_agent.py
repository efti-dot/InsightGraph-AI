from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState
from app.tools.csv_analyzer import analyze_csv


SYSTEM_PROMPT = """You are a data analyst. Given raw pandas summary
statistics for one or more CSV files, write 3-6 concise bullet points
interpreting the numbers as they relate to the research goal — trends,
growth, notable highs/lows, and any data quality issues like missing
values. Only use the numbers given; do not invent figures."""

def data_agent_node(state: ResearchState) -> ResearchState:
    csv_paths = state.get("csv_paths", [])

    if not csv_paths:
        if not csv_paths:
            print("[data_agent] skipped (no files)")
            return {"csv_analysis": "No CSV files were uploaded for this project."}

    goal = state.get("research_goal", "")

    summaries = []
    for path in csv_paths:
        try:
            summaries.append(analyze_csv(path))
        except Exception as exc:  # malformed CSV shouldn't crash the whole run
            summaries.append({"file": path, "error": str(exc)})

    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.2)
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Research goal:\n{goal}\n\nRaw statistics:\n{summaries}"),
        ]
    )

    print("[data_agent] analysis complete")
    return {"csv_analysis": response.content}