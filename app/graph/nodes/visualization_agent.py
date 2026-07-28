from app.graph.state import ResearchState
from app.tools.chart_builder import build_charts_for_csv

def visualization_agent_node(state: ResearchState) -> ResearchState:
    csv_paths = state.get("csv_paths", [])

    if not csv_paths:
        print("[visualization_agent] skipped (no CSVs)")
        return {"charts": []}