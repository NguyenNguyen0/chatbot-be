from typing import List
from fastapi import APIRouter, Depends, status

from app.services.ollama_service import chat_with_ollama, get_chat_section
from app.models.chat import ChatMessage, ChatResponse, ChatSection
from app.config import DEFAULT_MODEL
from app.middlewares.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
def chat(
    messages: List[ChatMessage],
    model: str = DEFAULT_MODEL,
    chat_id: str = None,
    user=Depends(get_current_user),
):
    return chat_with_ollama(user["user_id"], chat_id, messages, model)


@router.get("/{chat_id}", response_model=ChatSection, status_code=status.HTTP_200_OK)
def get_chat(chat_id: str, user_id: str = Depends(get_current_user)):
    return get_chat_section(user_id, chat_id)
