from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState
from app.tools.tavily_search import search_web

def web_agent_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")

    if not settings.tavily_api_key:
        state["web_findings"] = "Web search is not configured (no Tavily API key set)."
        state["status"] = "Web agent: skipped (no API key)"
        return state

    results = search_web(query=goal, max_results=5)