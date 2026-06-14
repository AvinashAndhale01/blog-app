from typing import Annotated
from fastapi import APIRouter, Depends
from app.model.user import User
from app.services.auth_service import get_current_active_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_current_user_profile(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user