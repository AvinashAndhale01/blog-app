from fastapi import APIRouter, HTTPException, Depends
from app.model.comment import Comment
from app.model.post import Post
from app.model.user import User
from app.schema.comment import CommentBase, CommentCreate, CommentPublic, CommentUpdate
from app.services.auth_service import get_current_user
from app.dependencies import SessionDep


router = APIRouter(prefix="/blogs", tags=["Comments"])


@router.get("/{post_id}/comments", response_model=list[CommentPublic])
def get_comments(post_id: int, session: SessionDep):
    post = session.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException(detail="Post not found", status_code=404)
    comments = session.query(Comment).filter(Comment.post_id==post_id)
    return comments



@router.post("/{post_id}/comments", response_model=CommentPublic)
def create_comment(post_id: int, comment: CommentCreate, session: SessionDep, current_user: User= Depends(get_current_user)):
    post = session.query(Post).filter(Post.id==post_id).first()
    if not post:
        raise HTTPException(detail="Post not found", status_code=404)
    comment_db = Comment(
        **comment.model_dump(), 
        post_id = post_id,
        user_id=current_user.id
    )
    session.add(comment_db)
    session.commit()
    session.refresh(comment_db)
    return comment_db


@router.delete("/{post_id}/comments/{comment_id}")
def delete_comment(post_id: int, comment_id: int, session: SessionDep, current_user: User=Depends(get_current_user)):
    comment = session.query(Comment).filter(Comment.id==comment_id, Comment.post_id==post_id).first()
    if not comment:
        raise HTTPException(detail="Comment not found", status_code=404)
    if not comment.user_id == current_user.id:
        raise HTTPException(detail="Not Authorized", status_code=403)
    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted successfully"}


@router.put("/{post_id}/comments/{comment_id}", response_model=CommentPublic)
def update_comment(post_id: int, comment_id: int, comment: CommentUpdate, session: SessionDep, current_user: User= Depends(get_current_user)):
    comment_db = session.query(Comment).filter(Comment.post_id==post_id, Comment.id==comment_id).first()
    if not comment_db:
        raise HTTPException(detail="Comment not found", status_code=404)
    if comment_db.user_id != current_user.id:
        raise HTTPException(detail="Not Authorized", status_code=403)
    comment_data = comment.model_dump()
    for key, value in comment_data.items():
        setattr(comment_db, key, value)
    session.commit()
    session.refresh(comment_db)
    return comment_db