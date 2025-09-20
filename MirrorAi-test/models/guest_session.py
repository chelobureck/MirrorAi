"""
Guest Session Model - управление кредитами гостей
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from models.base import Base

class GuestSession(Base):
    """Модель для хранения сессий гостей и их кредитов"""
    __tablename__ = "guest_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    credits = Column(Integer, default=50, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<GuestSession(session_id={self.session_id}, credits={self.credits})>"
