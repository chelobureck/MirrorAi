from __future__ import annotations
from typing import Optional
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, JSON, Boolean, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Presentation(Base):
    __tablename__ = "presentations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content: Mapped[dict] = mapped_column(JSON)  # Структура презентации
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    board_id: Mapped[Optional[int]] = mapped_column(ForeignKey("boards.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Поля для публичного доступа
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    public_id: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True, index=True)
    shared_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    views_count: Mapped[int] = mapped_column(Integer, default=0)

    # relationships
    user = relationship("User", back_populates="presentations")
    board = relationship("Board", back_populates="presentations")
    
