from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.config import settings
from app.graph.state import ResearchState

SYSTEM_PROMPT = """You are a fact checker comparing findings from three
research sources — internal documents, web search, and data analysis —
gathered for the same research goal. Identify places where sources report
conflicting facts or figures (e.g. different growth percentages, different
market size claims). List each conflict as a bullet point naming which
sources disagree and what each one says. Only flag genuine contradictions
— a source simply mentioning something the others don't is not a conflict.
If you find no contradictions, respond with exactly: "No conflicts detected
between sources." """

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
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_content),
        ]
    )

    print("[fact_checker] check complete")
    return {"conflicts": response.content}