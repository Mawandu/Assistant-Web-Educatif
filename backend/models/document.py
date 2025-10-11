from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from config.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    subject = Column(String, index=True)
    level = Column(String)
    status = Column(String, default="processing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
