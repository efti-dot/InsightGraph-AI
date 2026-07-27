from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.graph.state import ResearchState
from app.tools.pdf_retriever import retrieve_pdf_chunks
from app.config import settings


SYSTEM_PROMPT = """You are a research analyst summarizing findings extracted
from uploaded PDF documents. Given retrieved excerpts and a research goal,
write 3-6 concise bullet points of findings relevant to the goal. Only use
what's in the excerpts — if they don't contain relevant information, say so
plainly instead of making anything up."""


def pdf_agent_node(state: ResearchState) -> ResearchState:
    project_id = state.get("project_id", "default")
    goal = state.get("research_goal", "")
    uploaded_files = state.get("uploaded_files", [])

    if not uploaded_files:
        print("[pdf_agent] skipped (no files)")
        return {"pdf_findings": "No PDFs were uploaded for this project."}

    chunks = retrieve_pdf_chunks(project_id=project_id, query=goal, k=6)

    if not chunks:
        print("[pdf_agent] no matches")
        return {"pdf_findings": "PDFs were uploaded but no relevant content was retrieved for this goal."}

    context = "\n\n---\n\n".join(chunks)
    llm = ChatOpenAI(model=settings.model_name, api_key=settings.openai_api_key, temperature=0.2)
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Research goal:\n{goal}\n\nRetrieved excerpts:\n{context}"),
    ])

    print("[pdf_agent] findings extracted")
    return {"pdf_findings": response.content}