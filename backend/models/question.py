from pydantic import BaseModel, Field
from typing import Optional, List

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)
class Source(BaseModel):
    document: str
    page: Optional[int]

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]
    cached: bool = False