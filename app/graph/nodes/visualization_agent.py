from app.graph.state import ResearchState
from app.tools.chart_builder import build_charts_for_csv

def visualization_agent_node(state: ResearchState) -> ResearchState:
    csv_paths = state.get("csv_paths", [])

    if not csv_paths:
        print("[visualization_agent] skipped (no CSVs)")
        return {"charts": []}

    all_charts: list[dict] = []
    for path in csv_paths:
        try:
            all_charts.extend(build_charts_for_csv(path))
        except Exception as exc:
            print(f"[visualization_agent] failed on {path}: {exc}")

    print(f"[visualization_agent] built {len(all_charts)} chart(s)")
    return {"charts": all_charts}