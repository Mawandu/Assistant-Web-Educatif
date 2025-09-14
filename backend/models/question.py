from pydantic import BaseModel, Field
from typing import Optional, List

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=500)

# NOUVEAU: Modèle pour une source unique
class Source(BaseModel):
    document_id: Optional[int]
    page: Optional[int]

# NOUVEAU: Modèle pour la réponse complète
class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]