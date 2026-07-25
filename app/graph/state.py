from typing import TypedDict, List

class ResearchState(TypedDict, total=False):
    #s1
    project_id: str
    research_goal: str
    status: str
    draft_report: str