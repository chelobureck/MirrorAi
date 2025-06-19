from sqlalchemy import Column, Integer, String
from .base import Base

class UserPreferences(Base):
    __tablename__ = "userpreferences"

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String, default="light")
    language = Column(String, default="ru")
    default_template_id = Column(Integer, nullable=True) 