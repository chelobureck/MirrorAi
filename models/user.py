from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    username = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, default="user")  # user или guest
    credits = Column(Integer, default=0)
    presentations = relationship("Presentation", back_populates="user")
    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    email_verification_sent_at = Column(DateTime(timezone=True), nullable=True)
    email_verification_code = Column(String, nullable=True)
    preferences_id = Column(Integer, ForeignKey("userpreferences.id"), nullable=True) 