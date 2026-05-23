from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    description: str
    author: str

class PostCreate(PostBase):
    pass

class PostPublic(PostBase):
    id: int
    created_at: datetime
