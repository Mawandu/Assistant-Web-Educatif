from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.models.document import Document
from backend.api.dependencies import get_db
from backend.services.document_processor import extract_text_from_pdf, split_text_into_chunks
from backend.services.vector_store import VectorStore

router = APIRouter()

@router.post("/documents")
def create_document(file_name: str, subject: str, level: str, db: Session = Depends(get_db)):

    new_document = Document(file_name=file_name, subject=subject, level=level)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@router.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):

    documents = db.query(Document).all()
    return documents

@router.get("/documents/{doc_id}/process")
def process_document_text(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        return {"error": "Document non trouvé"}

    file_path = f"data/{document.file_name}"
    text = extract_text_from_pdf(file_path)
    chunks = split_text_into_chunks(text)

    try:
        vector_store = VectorStore()
        vector_store.add_document_chunks(doc_id=doc_id, chunks=chunks)

        return {
            "document_id": doc_id,
            "file_name": document.file_name,
            "status": "Traitement et vectorisation réussis.",
            "total_chunks_added": len(chunks)
        }
    except Exception as e:
        return {"error": f"Erreur lors de la vectorisation : {e}"}
