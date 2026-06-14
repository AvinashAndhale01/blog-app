from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import Base, engine
from app.routes import comment, posts, auth, users
from contextlib import asynccontextmanager
from app.model import User, Post, Comment


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.get("/status")
def status():
    return {"status": "ok"}


app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(comment.router)
app.include_router(users.router)
