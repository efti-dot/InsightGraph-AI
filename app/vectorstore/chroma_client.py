import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings

CHROMA_ROOT = os.path.join("storage", "chroma")

def safe_collection_name(project_id: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_" else "-" for c in project_id)
    return cleaned.strip("-_") or "default-project"


def get_collection(project_id: str) -> Chroma:
    collection_name = safe_collection_name(project_id)
    persist_dir = os.path.join(CHROMA_ROOT, collection_name)
    os.makedirs(persist_dir, exist_ok=True)

    embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)

    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )