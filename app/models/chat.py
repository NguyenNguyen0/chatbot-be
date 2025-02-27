from typing import List
from pydantic import BaseModel

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatSection(BaseModel):
    user_id: str
    chat_id: str
    messages: List[ChatMessage]
    model: str = "mistral"


class ChatResponse(BaseModel):
    chat_id: str
    response: str