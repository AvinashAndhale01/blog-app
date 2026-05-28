from app.core.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id=Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")