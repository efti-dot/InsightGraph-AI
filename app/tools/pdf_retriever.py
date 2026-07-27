from app.vectorstore.chroma_client import get_collection

def retrieve_pdf_chunks(project_id: str, query: str, k: int = 6) -> list[str]:
    collection = get_collection(project_id)
    docs = collection.similarity_search(query, k=k)

    return [doc.page_content for doc in docs]