from fastapi import FastAPI
from app.core.db import Base, engine
from app.routes import posts
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)



@app.get("/status")
def status():
    return {"status": "ok"}


app.include_router(posts.router)
