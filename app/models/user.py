from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str
    model: str = "mistral"


class ChatResponse(BaseModel):
    chat_id: str
    response: str
