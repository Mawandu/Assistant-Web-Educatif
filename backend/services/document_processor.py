import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict


def extract_pages_from_pdf(file_path: str) -> List[Dict]:
    """Extrait le contenu de chaque page et son numéro."""
    doc = fitz.open(file_path)
    pages_content = []
    for page_num, page in enumerate(doc):
        pages_content.append({
            "page_number": page_num + 1,
            "content": page.get_text()
        })
    return pages_content


def split_text_into_chunks(pages: List[Dict]) -> List[Dict]:
    """Découpe le texte de chaque page en morceaux en conservant les métadonnées."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    all_chunks = []
    for page in pages:
        chunks_on_page = text_splitter.split_text(page["content"])
        for chunk in chunks_on_page:
            all_chunks.append({
                "text": chunk,
                "metadata": {"page": page["page_number"]}
            })
            
    return all_chunks