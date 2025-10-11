# backend/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """
    PROJECT_NAME: str = "Assistant Web Éducatif"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres/assistantWed_db"
    
    OLLAMA_HOST: str = "http://ollama:11434"
    OLLAMA_MODEL: str = "tinyllama"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()