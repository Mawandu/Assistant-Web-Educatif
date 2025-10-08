# backend/models/user.py

import enum
from sqlalchemy import Column, Integer, String, Enum
from backend.config.database import Base
from pydantic import BaseModel


# Crée un type personnalisé pour le rôle, garantissant que seules ces valeurs sont acceptées
class RoleEnum(enum.Enum):
    student = "étudiant"
    teacher = "enseignant"
    admin = "administrateur"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # On ne stocke jamais le mot de passe en clair, seulement sa version hachée
    hashed_password = Column(String, nullable=False) 
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.student)

    # Modèle pour la création d'un utilisateur (ce que l'API reçoit)
class UserCreate(BaseModel):
    email: str
    password: str

# Modèle pour la réponse de l'API (ce que l'on renvoie, sans le mot de passe)
class UserResponse(BaseModel):
    id: int
    email: str
    role: RoleEnum

    class Config:
        from_attributes = True

# Modèle pour le jeton JWT
class Token(BaseModel):
    access_token: str
    token_type: str
