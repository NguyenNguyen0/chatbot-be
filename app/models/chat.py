from typing import List
from pydantic import BaseModel, Field

from app.config import settings

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message", example="user")
    content: str = Field(..., description="Message content", example="Hello!")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello!"
            }
        }


class ChatSection(BaseModel):
    user_id: str
    chat_id: str
    messages: List[ChatMessage]
    model: str = settings.DEFAULT_MODEL


class ChatResponse(BaseModel):
    chat_id: str
    response: str