from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings

# Crée le moteur de connexion à la base de données
engine = create_engine(
    settings.DATABASE_URL
)

# Crée une session locale pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base utilisée pour créer les modèles de tables de la base de données
Base = declarative_base()
