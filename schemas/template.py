from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[Dict[str, Any]] = None

class TemplateResponse(TemplateBase):
    id: int
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
