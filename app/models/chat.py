from typing import List
from pydantic import BaseModel, Field

from app.config import settings


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message", example="user")
    content: str = Field(..., description="Message content", example="Hello!")

    class Config:
        json_schema_extra = {"example": {"role": "user", "content": "Hello!"}}


class ChatRequest(BaseModel):
    chat_id: str | None = Field(None, description="Chat ID", example="67890")
    model: str = Field(
        default=settings.DEFAULT_MODEL,
        description="Model name",
        example=settings.DEFAULT_MODEL,
    )
    messages: List[ChatMessage] = Field(
        ...,
        description="List of messages",
        example=[ChatMessage(role="user", content="Hello!")],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "chat_id": "67890",
                "model": settings.DEFAULT_MODEL,
                "messages": [
                    {"role": "user", "content": "Hello!"},
                    {"role": "assistant", "content": "How are you?"},
                ],
            }
        }


class ChatResponse(BaseModel):
    chat_id: str = Field(..., description="Chat ID", example="67890")
    title: str | None = Field(None, description="Chat title", example="My Chat")
    response: str = Field(
        ...,
        description="Response from the model",
        example="Hello! How can I assist you?",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "chat_id": "67890",
                "title": "My Chat",
                "response": "Hello! How can I assist you?",
            }
        }


class ChatSection(BaseModel):
    user_id: str = Field(..., description="User ID", example="12345")
    chat_id: str = Field(..., description="Chat ID", example="67890")
    title: str = Field(..., description="Title of the chat", example="My Chat")
    created_at: str = Field(
        ..., description="Creation timestamp", example="2023-10-01T12:00:00Z"
    )
    model: str = Field(
        ..., description="Model used for the chat", example=settings.DEFAULT_MODEL
    )
    messages: List[ChatMessage] = Field(..., description="List of chat messages")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "12345",
                "chat_id": "67890",
                "title": "My Chat",
                "created_at": "2023-10-01T12:00:00Z",
                "model": settings.DEFAULT_MODEL,
                "messages": [
                    {"role": "user", "content": "Hello!"},
                    {
                        "role": "assistant",
                        "content": "Hi there! How can I help you today?",
                    },
                ],
            }
        }


class UserChatList(BaseModel):
    user_id: str = Field(..., description="User ID", example="12345")
    chats: List[ChatSection] = Field(..., description="List of chat sections")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "12345",
                "chats": [
                    {
                        "chat_id": "67890",
                        "title": "My Chat",
                        "created_at": "2023-10-01T12:00:00Z",
                        "model": settings.DEFAULT_MODEL,
                        "messages": [
                            {"role": "user", "content": "Hello!"},
                            {
                                "role": "assistant",
                                "content": "Hi there! How can I help you today?",
                            },
                        ],
                    }
                ],
            }
        }


class BotModel(BaseModel):
    name: str = Field(..., description="Model name", example="llama2")
    size: str = Field(..., description="Model size", example="7B")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "llama2",
                "size": "7B",
            }
        }


class BotModelResponse(BaseModel):
    models: List[BotModel] = Field(..., description="List of available models")
    total: int = Field(..., description="Total number of models", example=2)

    class Config:
        json_schema_extra = {
            "example": {
                "models": [
                    {"name": "llama2", "size": "7B"},
                    {"name": "llama3", "size": "13B"},
                ],
                "total": 2,
            }
        }


class RenameResponse(BaseModel):
    chat_id: str = Field(..., description="Chat ID", example="67890")
    title: str = Field(..., description="New chat title", example="My New Chat")
    success: bool = Field(..., description="Indicates if the rename was successful", example=True)

    class Config:
        json_schema_extra = {
            "example": {
                "chat_id": "67890",
                "title": "My New Chat",
                "success": True,
            }
        }