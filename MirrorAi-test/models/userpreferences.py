from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class UserPreferences(Base):
    __tablename__ = "userpreferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    default_theme = Column(String, default="modern")
    default_slide_count = Column(Integer, default=10)
    preferred_ai_provider = Column(String, default="groq")
    preferences = Column(JSON, nullable=True)  # Дополнительные настройки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    user = relationship("User", back_populates="preferences")
