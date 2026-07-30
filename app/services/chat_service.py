from langchain_core.tools import tool
from app.tools.pdf_retriever import retrieve_pdf_chunks
from app.tools.csv_query import CSV_TOOLS


def build_tools(project_id: str):
    @tool
    def search_documents(query: str) -> str:
        chunks = retrieve_pdf_chunks(project_id=project_id, query=query, k=6)
        if not chunks:
            return "No relevant content found in the uploaded PDFs."
        return "\n\n---\n\n".join(chunks)

    return [search_documents, *CSV_TOOLS]

def ask_followup(state: dict) -> str:
    project_id = state.get("project_id", "default")
    tools = build_tools(project_id)
    tools_by_name = {t.name: t for t in tools}