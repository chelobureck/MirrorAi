from pydantic import BaseModel
from typing import Optional

class TemplateResponse(BaseModel):
    id: int
    name: str
    preview_image_url: str
    is_popular: bool
    description: Optional[str] = None

    class Config:
        from_attributes = True 