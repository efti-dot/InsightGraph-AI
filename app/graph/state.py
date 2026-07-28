from typing import TypedDict, List

class ResearchState(TypedDict, total=False):
    #s1
    project_id: str
    research_goal: str
    status: str
    draft_report: str

    #s2
    uploaded_files: List[str]
    pdf_findings: str

    #s3
    web_findings: str

    #s4
    csv_paths: List[str]
    csv_analysis: str