from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.graph.state import ResearchState

def report_writer_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")

    llm = ChatOpenAI(
        model="",
        api_key="",
        temperature=0.3,
    )

    response = llm.invoke(
        [
            SystemMessage(content=""),
            HumanMessage(content=f"Research goal:\n{goal}"),
        ]
    )

    state["draft_report"] = response.content
    state["status"] = "Report writer: draft complete"
    return state