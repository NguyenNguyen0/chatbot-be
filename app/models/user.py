from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    is_active: bool = True
    last_login: str = None
    created_at: str = None


class UserRegisterRequest(BaseModel):
    name: str = Field(..., description="Username for registration", example="john_doe")
    password: str = Field(
        ..., description="User password", example="secure_password123"
    )

    class Config:
        json_schema_extra = {
            "example": {"name": "john_doe", "password": "secure_password123"}
        }


class UserLoginRequest(BaseModel):
    name: str = Field(..., description="Username for login", example="john_doe")
    password: str = Field(
        ..., description="User password", example="secure_password123"
    )

    class Config:
        json_schema_extra = {
            "example": {"name": "john_doe", "password": "secure_password123"}
        }
