from fastapi import APIRouter, HTTPException, Depends
from app.model import Post, User
from app.schema.post import PostCreate, PostPublic, PostUpdate
from app.dependencies import SessionDep
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=PostPublic, status_code=201)
def create_blog(post: PostCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    db_post = Post(**post.model_dump())
    db_post.user_id = current_user.id
    db_post.author = current_user.name
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
    blog = session.query(Post).filter( Post.id==id).first()
    if not blog:
        raise HTTPException(status_code=400, detail="Blog not found")
    return blog

@router.delete("/{id}")
def delete_blog(id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    blog = session.query(Post).filter(Post.user_id == current_user.id ,id==Post.id).first()
    if not blog:
        raise HTTPException(status_code=400, detail="Blog not found")
    session.delete(blog)
    session.commit()
    return {"msg":"Blog deleted successfully."}


@router.put("/{id}")
def update_blog(id: int, post: PostUpdate, session: SessionDep, current_user: User = Depends(get_current_user)):
    post_db = session.query(Post).filter(Post.id == id).first()
    if not post_db:
        raise HTTPException(status_code=404, detail="Blog not found")
    if post_db.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    post_data = post.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(post_db, key, value)
    session.commit()
    session.refresh(post_db)
    return post_db