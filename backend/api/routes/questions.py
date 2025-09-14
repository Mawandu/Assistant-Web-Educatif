from fastapi import APIRouter
# MODIFIÉ: Import des nouveaux modèles
from backend.models.question import QuestionRequest, QuestionResponse
from backend.services.question_handler import QuestionHandler

router = APIRouter()
handler = QuestionHandler()

# MODIFIÉ: Utilisation du response_model pour garantir le format de sortie
@router.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    """
    Receives a question, finds context, and returns an AI-generated answer.
    """
    answer_data = handler.get_answer(request.question)
    return answer_data