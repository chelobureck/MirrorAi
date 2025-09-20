from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from .base import Base

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(JSON, nullable=False)  # Полная копия презентации
    html_content = Column(String, nullable=True)  # Готовый HTML для быстрого доступа
    original_presentation_id = Column(Integer, ForeignKey("presentations.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False, default="")  # Имя шаблона (для совместимости с БД)
    preview_image_url = Column(String, nullable=False, default="")  # URL превью-картинки шаблона
    
    # Связи
    original_presentation = relationship("Presentation")
    user = relationship("User")