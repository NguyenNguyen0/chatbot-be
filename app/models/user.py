from pydantic import BaseModel, Field


class UserInDB(BaseModel):
    user_id: str
    username: str
    email: str
    password: str
    avatar: str | None = None  # base64 encoded image
    is_active: bool = True
    last_login: str = None
    created_at: str = None


class UserBasicInfo(BaseModel):
    user_id: str
    username: str
    email: str
    avatar: str | None = None  # base64 encoded image


class UserRegisterRequest(BaseModel):
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


class UserLoginRequest(BaseModel):
    username: str = Field(..., description="Username for login", example="abc")
    password: str = Field(..., description="User password", example="abc123")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "abc",
                "password": "abc123"
            }
        }


class UserLoginResponse(BaseModel):
    user_id: str
    access_token: str
    token_type: str = "bearer"


class UserRegisterResponse(BaseModel):
    message: str = "User registered successfully"
    access_token: str
