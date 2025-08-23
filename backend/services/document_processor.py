import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_path: str) -> str:
    # ... (cette fonction ne change pas)
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Erreur lors de l'extraction du PDF {file_path}: {e}")
        return ""

def split_text_into_chunks(text: str) -> list[str]:
    """
    Découpe un long texte en morceaux plus petits.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # La taille de chaque morceau
        chunk_overlap=200, # Le nombre de caractères de chevauchement
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
