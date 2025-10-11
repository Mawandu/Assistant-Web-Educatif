# backend/models/feedback.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    # Note: 1 pour un vote positif (👍), -1 pour un vote négatif (👎)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())