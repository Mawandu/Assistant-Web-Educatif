from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
import aiofiles
import os

from models.document import Document
from api.dependencies import get_db
from services.document_processor import extract_pages_from_pdf, split_text_into_chunks
from services.vector_store import VectorStore
from models.user import User as UserModel, RoleEnum
from api.dependencies import get_current_user


router = APIRouter()

UPLOAD_DIRECTORY = "data/documents"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/documents")
async def create_and_process_document(
    db: Session = Depends(get_db),
    subject: str = Form(...),
    level: str = Form(...),
    file: UploadFile = File(...),
    current_user: UserModel = Depends(get_current_user)
):  
    if current_user.role not in [RoleEnum.teacher, RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action non autorisée. Seuls les enseignants et administrateurs peuvent ajouter des documents."
        )
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier : {e}")

    new_document = Document(file_name=file.filename, subject=subject, level=level)
    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    try:
        # MODIFIÉ: Utilise les nouvelles fonctions pour le traitement
        pages = extract_pages_from_pdf(file_path)
        chunks = split_text_into_chunks(pages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'extraction du texte du PDF : {e}")

    try:
        vector_store = VectorStore()
        vector_store.add_document_chunks(doc_id=new_document.id, chunks=chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vectorisation : {e}")

    return {
        "message": "Document téléversé et traité avec succès !",
        "document_details": {
            "id": new_document.id,
            "file_name": new_document.file_name,
            "subject": new_document.subject,
            "level": new_document.level,
            "chunks_added": len(chunks)
        }
    }

@router.get("/documents")
def get_all_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents