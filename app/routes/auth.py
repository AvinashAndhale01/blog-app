from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.model.user import User
from app.schema.user import UserCreate, UserPublic
from app.schema.auth import Token
from app.dependencies import SessionDep
from app.core.security import get_password_hash, create_access_token
from app.services.auth_service import authenticate_user
from datetime import timedelta
from app.core.config import setting


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


@router.post("/login", response_model=Token)
def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expire = timedelta(minutes=setting.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.email}, expire_delta=access_token_expire)
    return Token(access_token=access_token, token_type="bearer")
    