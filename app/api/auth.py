from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.auth_service import register_user, login_user, get_user, logout_user
from app.models.user import UserRegisterRequest, UserLoginRequest, UserLoginResponse, UserRegisterResponse, UserBasicInfo

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security = HTTPBearer()

@router.post(
    "/register",
    response_model=UserRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user with a unique username and a password",
)
def register(user_request: UserRegisterRequest):
    return register_user(user_request.username, user_request.email, user_request.password, user_request.confirm_password)


@router.post(
    "/login",
    response_model=UserLoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    description="Login a user with a valid username and password",
)
def login(user_request: UserLoginRequest):
    return login_user(user_request.username, user_request.password)


@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=UserBasicInfo,
    summary="Get authenticated user",
    description="Get details of the currently authenticated user details by token"
)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return get_user(credentials.credentials)


@router.post('/logout',
    status_code=status.HTTP_200_OK,
    summary="Logout a user",
    description="Logout a user"
)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return logout_user(credentials.credentials)