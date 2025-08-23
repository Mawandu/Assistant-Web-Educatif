from pydantic import BaseModel, Field
from typing import Optional

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
    context: Optional[str] = None
    user_id: Optional[str] = None
