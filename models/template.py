from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    preview_image_url = Column(String, nullable=False)
    is_popular = Column(Boolean, default=False)
    description = Column(String, nullable=True) 