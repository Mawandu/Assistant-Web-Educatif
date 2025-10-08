from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the application.
    """
    PROJECT_NAME: str = "Assistant Web Éducatif"
    API_V1_STR: str = "/api/v1"

    # Base de données (PostgreSQL)
    DATABASE_URL: str = "postgresql://postgres:postgres@postgres/assistantWed_db"

    class Config:
        case_sensitive = True
        # Permet de lire les variables depuis un fichier .env
        env_file = ".env"

settings = Settings()
