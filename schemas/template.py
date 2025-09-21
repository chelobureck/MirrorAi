from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import Column

class TemplateCreate(BaseModel):
    presentation_id: int

class TemplateSaveRequest(BaseModel):
    """Запрос для сохранения презентации как шаблона с данными"""
    presentation_id: Optional[int] = None  # Опционально, если есть ID в БД
    title: Optional[str] = None  # Опционально - если None, извлекается из презентации
    html: Optional[str] = None   # Опционально - если None, извлекается из презентации
    description: Optional[str] = None  # Опциональное описание

class TemplateResponse(BaseModel):
    templateId: str  # public_id
    title: str
    createdAt: Column[datetime]
    
    class Config:
        from_attributes = True

class TemplateDetail(BaseModel):
    templateId: str  # public_id  
    html: str
    title: str
    
class TemplateCreateResponse(BaseModel):
    templateId: str  # public_id
    message: str = "Template created successfully"
    
class TemplateDeleteResponse(BaseModel):
    message: str = "Template deleted successfully"
