from fastapi import APIRouter, HTTPException
from app.model.user import User
from app.schema.user import UserCreate, UserPublic
from app.dependencies import SessionDep
from app.core.security import get_password_hash


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    db_user = session.query(User).filter(user.email == User.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exist try dfferent email id")
    user.password = get_password_hash(user.password)
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user