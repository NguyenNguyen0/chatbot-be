from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: str
    username: str
    email: str
    password: str
    is_active: bool = True
    last_login: str = None
    created_at: str = None


class UserRegisterRequest(BaseModel):
    username: str = Field(..., description="Username for registration", example="abc")
    password: str = Field(
        ..., description="User password", example="abc123"
    )

    class Config:
        json_schema_extra = {
            "example": {"name": "abc", "password": "abc123"}
        }


class UserLoginRequest(BaseModel):
    username: str = Field(..., description="Username for login", example="abc")
    password: str = Field(
        ..., description="User password", example="abc123"
    )

    class Config:
        json_schema_extra = {
            "example": {"username": "abc", "password": "abc123"}
        }

class UserLoginResponse(BaseModel):
    user_id: str
    access_token: str
    token_type: str = 'bearer'