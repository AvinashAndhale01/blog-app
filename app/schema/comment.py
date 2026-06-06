from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    title: str


class CommentPublic(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass