from fastapi import APIRouter, HTTPException
from app.model.post import Post
from app.schema.post import PostCreate, PostPublic
from app.dependencies import SessionDep

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=PostPublic, status_code=201)
def create_blog(post: PostCreate, session: SessionDep):
    db_post = Post(**post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostPublic])
def get_blogs(session: SessionDep):
    all_blog = session.query(Post).all()
    return all_blog

@router.get("/{id}", response_model=PostPublic)
def get_blog(id: int, session: SessionDep):
    blog = session.query(Post).filter(Post.id==id).first()
    return blog

@router.delete("/{id}")
def delete_blog(id: int, session: SessionDep):
    blog = session.query(Post).filter(id==Post.id).first()
    if not blog:
        raise HTTPException(status_code=400, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return {"msg":"Blog deleted successfully."}