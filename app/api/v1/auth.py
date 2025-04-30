from fastapi import APIRouter, status, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.auth_service import register_user, login_user, get_user, logout_user, refresh_user_access_token
from app.models.user import RegistrationRequest, LoginCredentials, AuthTokenResponse, RegistrationSuccessResponse, UserProfile, TokenRefreshResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security = HTTPBearer()

@router.post(
    "/register",
    response_model=RegistrationSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user with a unique username and a password",
)
def register(user_request: RegistrationRequest):
    return register_user(user_request.username, user_request.email, user_request.password, user_request.confirm_password)


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    description="Login a user with a valid username and password",
)
def login(user_request: LoginCredentials):
    return login_user(user_request.username, user_request.password)


@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=UserProfile,
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
def logout(
    access_token: str = Body(..., description="Access token", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
    refresh_token: str = Body(..., description="Refresh token", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
):
    return logout_user(access_token=access_token, refresh_token=refresh_token)


@router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    response_model=TokenRefreshResponse,
    summary="Refresh access token",
    description="Refresh the access token using the refresh token",
)
def refresh_token(
    refresh_token: str = Body(..., description="Refresh token", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
):
    return refresh_user_access_token(refresh_token)