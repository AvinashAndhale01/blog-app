from fastapi import Depends, HTTPException, status
from app.dependencies import SessionDep
from typing import Annotated
from app.model.user import User
from sqlalchemy.orm import Session
from app.core.security import verify_password, DUMMY_HASH
from fastapi.security import OAuth2PasswordBearer
from app.core.config import setting
from app.schema.auth import TokenData
import jwt
from jwt.exceptions import InvalidTokenError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_user(email: str, session: Session):
    return session.query(User).filter(email == User.email).first()


def authenticate_user(session: Session, email: str, password: str):
    user = get_user(email, session)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, setting.secret_key, algorithms=[setting.algorithm])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.email, SessionDep)
    if user is None:
        raise credentials_exception
    return user