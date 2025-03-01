from typing import List
from fastapi import APIRouter, Depends

from app.services.ollama_service import (
    chat_with_ollama,
    get_chat_section
)
from app.models.chat import ChatMessage, ChatResponse, ChatSection
from app.config import DEFAULT_MODEL
from app.middlewares.auth import get_current_user

router = APIRouter()


@router.post("/{user_id}")
def chat(
    messages: List[ChatMessage],
    model: str = DEFAULT_MODEL,
    chat_id: str = None,
    user=Depends(get_current_user),
) -> ChatResponse:
    return chat_with_ollama(user['user_id'], chat_id, messages, model)


@router.get("/{user_id}/{chat_id}")
def get_chat(user_id: str, chat_id: str) -> ChatSection:
    return get_chat_section(user_id, chat_id)
