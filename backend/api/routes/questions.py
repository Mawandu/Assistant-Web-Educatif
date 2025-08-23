from fastapi import APIRouter
from backend.models.question import QuestionRequest
from backend.services.question_handler import QuestionHandler

router = APIRouter()
handler = QuestionHandler()

@router.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Receives a question, finds context, and returns an AI-generated answer.
    """
    answer_data = handler.get_answer(request.question)
    return answer_data
