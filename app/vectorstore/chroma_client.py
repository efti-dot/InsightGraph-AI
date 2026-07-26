import os
from langchain_chroma import Chroma

CHROMA_ROOT = os.path.join("storage", "chroma")

def safe_collection_name(project_id: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_" else "-" for c in project_id)
    return cleaned.strip("-_") or "default-project"