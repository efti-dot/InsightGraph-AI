from app.graph.state import ResearchState
from app.graph.build_graph import research_graph

def start_run(project_id: str, research_goal: str) -> ResearchState:
    initial_state: ResearchState = {
        "project_id": project_id,
        "research_goal": research_goal,
        "status": "starting",
    }

    final_state = research_graph.invoke(initial_state)
    return final_state