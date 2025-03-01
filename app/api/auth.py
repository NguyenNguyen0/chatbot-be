from fastapi import APIRouter, Depends

from app.services.auth_service import register_user, login_user
from app.models.user import UserRegisterRequest, UserLoginRequest

router = APIRouter()


@router.post("/register")
def register(user_request: UserRegisterRequest):
    return register_user(user_request.name, user_request.password)


@router.post("/login")
def login(user_request: UserLoginRequest):
    return login_user(user_request.name, user_request.password)
