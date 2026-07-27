from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState
from app.tools.tavily_search import search_web


SYSTEM_PROMPT = """You are a research analyst summarizing recent web search
results (news, policy, competitor activity) relevant to a research goal.
Given a list of search results, write 3-6 concise bullet points of findings.
Mention the source (by title or domain) for each point where useful. If the
results don't contain relevant information, say so plainly instead of
making anything up."""


def web_agent_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")

    if not settings.tavily_api_key:
        state["web_findings"] = "Web search is not configured (no Tavily API key set)."
        state["status"] = "Web agent: skipped (no API key)"
        return state

    results = search_web(query=goal, max_results=5)
    if not results:
        state["web_findings"] = "Web search returned no relevant results for this goal."
        state["status"] = "Web agent: no results"
        return state

    formatted = "\n\n".join(
        f"Title: {r.get('title', 'Untitled')}\nURL: {r.get('url', '')}\nContent: {r.get('content', '')}"
        for r in results
    )

    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.2)
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Research goal:\n{goal}\n\nSearch results:\n{formatted}"),
        ]
    )

    state["web_findings"] = response.content
    state["status"] = "Web agent: findings extracted"
    return state