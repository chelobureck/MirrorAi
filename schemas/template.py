from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TemplateCreate(BaseModel):
    presentation_id: int

class TemplateSaveRequest(BaseModel):
    """Запрос для сохранения презентации как шаблона с данными"""
    presentation_id: Optional[int] = None
    title: Optional[str] = None
    html: Optional[str] = None
    description: Optional[str] = None

class TemplateResponse(BaseModel):
    templateId: str  # public_id
    title: str
    createdAt: datetime
    
    class Config:
        from_attributes = True

class TemplateDetail(BaseModel):
    templateId: str
    html: str
    title: str
    
class TemplateCreateResponse(BaseModel):
    templateId: str
    message: str = "Template created successfully"
    
class TemplateDeleteResponse(BaseModel):
    message: str = "Template deleted successfully"

