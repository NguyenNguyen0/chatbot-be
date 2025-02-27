from typing import List
from fastapi import APIRouter, Depends

from app.services.ollama_service import chat_with_ollama, get_chat_section
from app.models.chat import ChatMessage, ChatResponse, ChatSection
from app.config import DEFAULT_MODEL

router = APIRouter()


@router.post("/")
def chat(
    user_id: str, chat_id: str, messages: List[ChatMessage], model: str = DEFAULT_MODEL
) -> ChatResponse:
    return chat_with_ollama(user_id, chat_id, messages, model)


@router.get("/{chat_id}")
def get_chat(user_id: str, chat_id: str) -> ChatSection:
    return get_chat_section(user_id, chat_id)
