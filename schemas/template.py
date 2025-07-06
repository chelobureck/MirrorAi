from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TemplateCreate(BaseModel):
    presentation_id: int

class TemplateResponse(BaseModel):
    templateId: str  # public_id
    title: str
    createdAt: datetime
    
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
