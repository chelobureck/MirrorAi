from pydantic import BaseModel
from typing import Optional

class UserPreferencesResponse(BaseModel):
    theme: str
    language: str
    default_template_id: Optional[int] = None

class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    default_template_id: Optional[int] = None 