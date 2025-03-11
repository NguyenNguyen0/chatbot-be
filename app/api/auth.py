from fastapi import APIRouter, status

from app.services.auth_service import register_user, login_user
from app.models.user import UserRegisterRequest, UserLoginRequest, UserLoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_request: UserRegisterRequest):
    return register_user(user_request.name, user_request.password)


@router.post("/login", response_model=UserLoginResponse , status_code=status.HTTP_200_OK)
def login(user_request: UserLoginRequest):
    return login_user(user_request.name, user_request.password)
