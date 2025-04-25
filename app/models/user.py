from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class DBUser(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user", example="usr_12345abcde")
    username: str = Field(..., description="User's chosen username", example="johndoe")
    email: EmailStr = Field(..., description="User's email address", example="john.doe@example.com")
    password: str = Field(..., description="Hashed password - never returned to clients", example="$2b$12$...")
    avatar: Optional[str] = Field(None, description="Base64 encoded profile image", example="data:image/jpeg;base64,...")
    is_active: bool = Field(True, description="Whether the user account is active")
    last_login: Optional[str] = Field(None, description="ISO timestamp of last login", example="2025-04-12T15:30:45Z")
    created_at: Optional[str] = Field(None, description="ISO timestamp of account creation", example="2025-04-01T12:00:00Z")

    class Config:
        json_schema_extra = {
            "example": {
                "example": {
                    "user_id": "usr_12345abcde",
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "password": "$2b$12$...",
                    "avatar": "data:image/jpeg;base64,...",
                    "is_active": True,
                    "last_login": "2025-04-12T15:30:45Z",
                    "created_at": "2025-04-01T12:00:00Z"
                }
            }
        }


class UserProfile(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user", example="usr_12345abcde")
    username: str = Field(..., description="User's chosen username", example="johndoe")
    email: EmailStr = Field(..., description="User's email address", example="john.doe@example.com")
    avatar: Optional[str] = Field(None, description="Base64 encoded profile image", example="data:image/jpeg;base64,...")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "usr_12345abcde",
                "username": "johndoe",
                "email": "john.doe@example.com",
                "avatar": "data:image/jpeg;base64,..."
            }
        }


class RegistrationRequest(BaseModel):
    username: str = Field(..., description="Username for registration", example="abc")
    email: str = Field(
        ..., description="Email for registration", example="abc@gmail.com"
    )
    password: str = Field(..., description="User password", example="abc123")
    confirm_password: str = Field(
        ..., description="User password confirmation", example="abc123"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc",
                "email": "abc@gmail.com",
                "password": "abc123",
                "confirm_password": "abc123"
            }
        }


class LoginCredentials(BaseModel):
    username: str = Field(..., description="Username for login", example="abc")
    password: str = Field(..., description="User password", example="abc123")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc",
                "password": "abc123"
            }
        }


class AuthTokenResponse(BaseModel):
    user_id: str = Field(
        ..., 
        description="Unique identifier for the authenticated user", 
        example="usr_12345abcde"
    )
    access_token: str = Field(
        ..., 
        description="JWT token for authenticating subsequent requests", 
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    refresh_token: Optional[str] = Field(
        None,
        description="Refresh token for obtaining a new access token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(
        "bearer", 
        description="Type of authentication token",
        example="bearer"
    )

    class Config:
        json_shema_extra = {
            "example": {
                "user_id": "usr_12345abcde",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class RegistrationSuccessResponse(BaseModel):
    message: str = Field(
        "User registered successfully", 
        description="Status message indicating successful registration"
    )
    access_token: str = Field(
        None, 
        description="JWT token for authenticating subsequent requests", 
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    refresh_token: Optional[str] = Field(
        None,
        description="Refresh token for obtaining a new access token",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )
    token_type: str = Field(
        "bearer", 
        description="Type of authentication token",
        example="bearer"
    )


    class Config:
        json_schema_extra = {
            "example": {
                "message": "User registered successfully",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenRefreshResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="New JWT token for authenticating subsequent requests",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }