from app.graph.state import ResearchState
from app.graph.build_graph import research_graph
from app.services.ingestion_service import ingest_pdfs
import os

def start_run(project_id: str, research_goal: str, pdf_paths: list[str] | None=None,) -> ResearchState:
    pdf_paths = pdf_paths or []
    if pdf_paths:
        ingest_pdfs(project_id=project_id, pdf_paths=pdf_paths)

    initial_state: ResearchState = {
        "project_id": project_id,
        "research_goal": research_goal,
        "uploaded_files": [os.path.basename(p) for p in pdf_paths],
        "status": "starting",
    }

    final_state = research_graph.invoke(initial_state)
    return final_state