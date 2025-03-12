from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from app.database import users_collection
from fastapi import HTTPException
from app.config import settings
from app.models.user import UserLoginResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def register_user(username: str, password: str):
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    user_id = users_collection.insert_one(
        {"username": username, "password": hashed_password}
    ).inserted_id
    return {"message": "User registered successfully", "user_id": str(user_id)}


def login_user(username: str, password: str) -> UserLoginResponse:
    user = users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"user_id": str(user["_id"])})
    return UserLoginResponse(user_id=str(user["_id"]), access_token=access_token)
