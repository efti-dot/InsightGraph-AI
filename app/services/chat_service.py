from langchain_core.tools import tool
from app.tools.pdf_retriever import retrieve_pdf_chunks
from app.tools.csv_query import CSV_TOOLS
from langchain_openai import ChatOpenAI
from app.config import settings


def build_tools(project_id: str):
    @tool
    def search_documents(query: str) -> str:
        chunks = retrieve_pdf_chunks(project_id=project_id, query=query, k=6)
        if not chunks:
            return "No relevant content found in the uploaded PDFs."
        return "\n\n---\n\n".join(chunks)

    return [search_documents, *CSV_TOOLS]

def build_system_prompt(state: dict) -> str:
    goal = state.get("research_goal", "")
    merged_knowledge = state.get("merged_knowledge", "") or "None available."
    csv_paths = state.get("csv_paths", [])
    chart_titles = [c.get("title", "") for c in state.get("charts", [])]

    csv_list = "\n".join(f"- {p}" for p in csv_paths) if csv_paths else "None uploaded."
    chart_list = ", ".join(chart_titles) if chart_titles else "None."

    return f"""You are answering follow-up questions about a completed
research project. Use the project context below and the tools available
to you — don't guess at exact numbers you could look up with a tool.

Research goal:
{goal}

Merged findings summary:
{merged_knowledge}

Available CSV files (pass the full path shown here to the CSV tools):
{csv_list}

Charts generated: {chart_list}

For questions about specific documents, use search_documents. For
questions about exact numbers, comparisons, or "which X has the
highest/lowest Y" — use the CSV tools instead of estimating from the
summary above (call list_columns first if you're unsure of column
names). Keep answers concise and conversational, like a colleague
answering a quick question, not another full report."""

def ask_followup(state: dict) -> str:
    project_id = state.get("project_id", "default")
    tools = build_tools(project_id)
    tools_by_name = {t.name: t for t in tools}

    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.2)
    llm_with_tools = llm.bind_tools(tools)

