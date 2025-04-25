from typing import List, Dict, Any
import logging
import ollama
from fastapi import HTTPException, status

from app.models.chat import ChatMessage
from app.config import settings


def send_chat_to_ollama(messages: List[ChatMessage], model: str = settings.DEFAULT_MODEL) -> str:
    messages_dict = [
        msg.model_dump() if isinstance(msg, ChatMessage) else msg for msg in messages
    ]

    try:
        response = ollama.chat(model=model, messages=messages_dict)
        return response["message"]["content"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to communicate with Ollama service: {str(e)}",
        )


def generate_chat_title(messages: List[ChatMessage], model: str = settings.DEFAULT_MODEL) -> str | None:
    messages_dict = [
        msg.model_dump() if isinstance(msg, ChatMessage) else msg for msg in messages
    ]

    if messages_dict[-1]["role"] != "assistant":
        logging.error("Last message must be from assistant", exc_info=True)
        return None
    
    if len(messages_dict) > 4:
        return None

    # Add prompt to generate title
    messages_dict.append({
        "role": "user",
        "content": (
            "Give the shortest possible title for this conversation. "
            "Use the same language as the conversation. "
            "Do not include any special characters, punctuation, or quotation marks. "
            "Keep it under 8 words."
        ),
    })

    try:
        response = ollama.chat(model=model, messages=messages_dict)
        return response["message"]["content"].replace('"', '')
    except Exception as e:
        logging.error(f"Failed to generate title: {str(e)}", exc_info=True)
        return None


def get_all_ollama_models() -> List[Dict[str, Any]]:
    try:
        response = ollama.list()
        return response.models
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch models from Ollama: {str(e)}",
        )
