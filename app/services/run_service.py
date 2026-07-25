from app.graph.state import ResearchState

def start_run(project_id: str, research_goal: str) -> ResearchState:
    initial_state: ResearchState = {
        "project_id": project_id,
        "research_goal": research_goal,
        "status": "starting",
    }