import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def split_text(text: str, chunk_size: int , chunk_overlap: int):
    """
    Divide el texto en chunks con control de tamaño y superposición.
    Usa RecursiveCharacterTextSplitter de LangChain. 
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    docs = text_splitter.create_documents([text])
    # Cada documento tiene .page_content con el texto del chunk
    return docs