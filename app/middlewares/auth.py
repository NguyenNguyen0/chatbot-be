from typing import Optional
from fastapi import Depends, HTTPException, Request, WebSocket
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings


class OptionalHTTPBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        try:
            return await super().__call__(request)
        except HTTPException:
            return None


security = HTTPBearer()
optional_security = OptionalHTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload  # payload chứa user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security),
):
    """Get current user information if token is valid, otherwise return None."""
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except (jwt.PyJWTError, AttributeError):
        return None


async def get_current_user_ws(websocket: WebSocket):
    print("\t ⭐ WebSocket query params:", websocket.query_params)
    auth_token = websocket.query_params.get("token")
    # Or from headers (e.g., for custom protocols)
    if not auth_token:
        auth_token = websocket.headers.get("authorization")
        if auth_token and auth_token.lower().startswith("bearer "):
            auth_token = auth_token[7:]

    if not auth_token:
        return None

    try:
        payload = jwt.decode(
            auth_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except (jwt.PyJWTError, AttributeError):
        return None