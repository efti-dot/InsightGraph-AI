from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState

def fact_checker_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    pdf_findings = state.get("pdf_findings", "") or "None"
    web_findings = state.get("web_findings", "") or "None"
    csv_analysis = state.get("csv_analysis", "") or "None"

    user_content = f"""Research goal:
{goal}

PDF findings:
{pdf_findings}

Web findings:
{web_findings}

Data analysis findings:
{csv_analysis}"""

    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.0)
    response = llm.invoke(
        [
            SystemMessage(content=""),
            HumanMessage(content=user_content),
        ]
    )

    print("[fact_checker] check complete")
    return {"conflicts": response.content}