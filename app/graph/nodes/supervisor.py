from app.graph.state import ResearchState

def supervisor_node(state: ResearchState) -> ResearchState:
    goal = state.get("research_goal", "")
    print(f"[supervisor] received goal: {goal}")

    state["status"] = "Supervisor: plan ready"
    return state