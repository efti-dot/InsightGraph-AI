from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.graph.state import ResearchState
from app.tools.pdf_retriever import retrieve_pdf_chunks
from app.config import settings

def pdf_agent_node(state: ResearchState) -> ResearchState:
    project_id = state.get("project_id", "default")
    goal = state.get("research_goal", "")
    uploaded_files = state.get("uploaded_files", [])

    if not uploaded_files:
        state["pdf_findings"] = "No PDFs were uploaded for this project."
        state["status"] = "PDF agent: skipped (no files)"
        return state

    chunks = retrieve_pdf_chunks(project_id=project_id, query=goal, k=6)

    if not chunks:
        state["pdf_findings"] = "PDFs were uploaded but no relevant content was retrieved for this goal."
        state["status"] = "PDF agent: no matches"
        return state

    context = "\n\n---\n\n".join(chunks)
    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.2)
    response = llm.invoke(
        [
            SystemMessage(content=""),
            HumanMessage(content=f"Research goal:\n{goal}\n\nRetrieved excerpts:\n{context}"),
        ]
    )

    state["pdf_findings"] = response.content
    state["status"] = "PDF agent: findings extracted"
    return state