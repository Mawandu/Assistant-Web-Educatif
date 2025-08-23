from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.api.routes import questions, documents
from backend.models import document 

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API pour l'assistant éducatif.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines (à changer pour la production)
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

app.include_router(questions.router, prefix=settings.API_V1_STR, tags=["Questions"])
app.include_router(documents.router, prefix=settings.API_V1_STR, tags=["Documents"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
