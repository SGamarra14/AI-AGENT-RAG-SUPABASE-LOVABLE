import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv

from pdf_utils import extract_text_from_pdf, split_text
from embeddings import get_embedding
from supabase_client import get_supabase

load_dotenv()

def ingest_pdf(
    pdf_path: str,
    chunk_size: int,
    chunk_overlap: int
):
    supabase = get_supabase()

    full_text = extract_text_from_pdf(pdf_path)
    docs = split_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for idx, doc in enumerate(docs):
        chunk_text = doc.page_content.strip()
        if not chunk_text:
            continue

        embedding = get_embedding(chunk_text)

        supabase.table("documents").insert({
            "content": chunk_text,
            "embedding": embedding,
            "metadata": {
                "source": os.path.basename(pdf_path),
                "chunk_index": idx,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap
            }
        }).execute()

    print(f" Ingestado: {pdf_path} | chunks: {len(docs)}")

if __name__ == "__main__":
    # Path portable (funciona en Windows y Linux/Render)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PDF_PATH = os.path.join(BASE_DIR, "data", "rag.pdf")

    ingest_pdf(PDF_PATH, chunk_size=900, chunk_overlap=200)