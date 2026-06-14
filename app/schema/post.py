from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    title: str
    description: str

class PostCreate(PostBase):
    pass

class PostPublic(PostBase):
    id: int
    author: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostUpdate(BaseModel):
    
    title: str | None = None
    description: str | None = None
