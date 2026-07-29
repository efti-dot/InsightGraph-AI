import os
from docx import Document

REPORTS_ROOT = os.path.join("storage", "reports")

def _report_dir(project_id: str) -> str:
    path = os.path.join(REPORTS_ROOT, project_id)
    os.makedirs(path, exist_ok=True)
    return path


def export_docx(project_id: str) -> str:
    out_dir = _report_dir(project_id)
    doc = Document()
