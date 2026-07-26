import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.vectorstore.chroma_client import get_collection

def _extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def  ingest_pdfs(project_id: str, pdf_paths: list[str]) -> int:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    collection = get_collection(project_id)

    texts: list[str] = []
    metadatas: list[dict] = []

    for path in pdf_paths:
        raw_text = _extract_text(path)
        if not raw_text.strip():
            continue

        chunks = splitter.split_text(raw_text)
        texts.extend(chunks)
        metadatas.extend({"source": os.path.basename(path)} for _ in chunks)

    if texts:
        collection.add_texts(texts=texts, metadatas=metadatas)

    return len(texts)