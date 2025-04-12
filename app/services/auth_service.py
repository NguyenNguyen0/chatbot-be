from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.database import users_collection
from fastapi import HTTPException, status
from bson import ObjectId

from app.config import settings
from app.models.user import UserLoginResponse, UserRegisterResponse, UserBasicInfo, UserRefreshTokenResponse
from app.database import token_blacklist

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def register_user(
    username: str, email: str, password: str, confirm_password: str
) -> UserRegisterResponse:
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    if users_collection.find_one({"username": username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Username already exists {username}"
        )
    if users_collection.find_one({"email": email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email already used {email}"
        )

    hashed_password = hash_password(password)
    user_id = users_collection.insert_one(
        {"username": username, "password": hashed_password, "email": email}
    ).inserted_id

    token = create_access_token({"user_id": str(user_id)})
    refresh_token = create_refresh_token({"user_id": str(user_id)})
    return UserRegisterResponse(
        message="User registered successfully", access_token=token, refresh_token=refresh_token
    )


def login_user(username: str, password: str) -> UserLoginResponse:
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not exists"
        )
    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    access_token = create_access_token({"user_id": str(user["_id"])})
    refresh_token = create_refresh_token({"user_id": str(user["_id"])})
    return UserLoginResponse(user_id=str(user["_id"]), access_token=access_token, refresh_token=refresh_token)


def get_user(token: str) -> UserBasicInfo:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    if token_blacklist.find_one({"token": token}):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated",
        )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Remove sensitive information
        user.pop("password", None)
        user["_id"] = str(user["_id"])

        return UserBasicInfo(
            user_id=user["_id"],
            username=user["username"],
            email=user["email"],
            avatar=user.get("avatar"),
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
        )


def logout_user(access_token: str, refresh_token: str):
    try:
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        exp_timestamp = payload.get("exp")

        # Add token to blacklist
        # TODO: implement by redis
        token_blacklist.insert_many([
            {
                "token": access_token,
                "expires_at": datetime.fromtimestamp(exp_timestamp, tz=timezone.utc),
            },
            {
                "token": refresh_token,
                "expires_at": datetime.fromtimestamp(exp_timestamp, tz=timezone.utc),
            }
        ])

        return {"message": "User logged out successfully"}
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def refresh_user_access_token(refresh_token: str) -> UserRefreshTokenResponse:
    try:
        if token_blacklist.find_one({"token": refresh_token}):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been invalidated",
            )
        
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid refresh token payload"
            )
            
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found"
            )
        
        new_access_token = create_access_token({"user_id": user_id})

        return UserRefreshTokenResponse(access_token=new_access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")