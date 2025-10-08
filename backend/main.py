from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.models import document 
from backend.api.routes import questions, documents, users,feedback

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API pour l'assistant éducatif.",
    version="0.1.0"
)

app.include_router(users.router, prefix="/api/v1", tags=["Users"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet toutes les origines (à changer pour la production)
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

app.include_router(questions.router, prefix="/api/v1", tags=["Questions"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])
app.include_router(feedback.router, prefix="/api/v1", tags=["Feedback"])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de l'Assistant Web Éducatif"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
