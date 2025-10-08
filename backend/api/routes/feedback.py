# backend/api/routes/feedback.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.api.dependencies import get_db, get_current_user
from backend.models.feedback import Feedback as FeedbackModel
from backend.models.user import User as UserModel

router = APIRouter()

class FeedbackCreate(BaseModel):
    question: str
    answer: str
    rating: int

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Permet à un utilisateur authentifié de donner son avis sur une réponse."""
    if feedback.rating not in [1, -1]:
        raise HTTPException(status_code=400, detail="La note doit être 1 ou -1.")

    new_feedback = FeedbackModel(
        question=feedback.question,
        answer=feedback.answer,
        rating=feedback.rating
    )
    db.add(new_feedback)
    db.commit()
    return {"message": "Merci pour votre retour !"}