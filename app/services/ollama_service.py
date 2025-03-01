from typing import List
import ollama
from fastapi import HTTPException

from app.database import chats_collection
from app.models.chat import ChatMessage, ChatResponse, ChatSection
from app.utils import generate_id
from app.config import DEFAULT_MODEL


def chat_with_ollama(
    user_id: str,
    chat_id: str,
    messages: List[ChatMessage],
    model: str = DEFAULT_MODEL,
) -> ChatResponse:
    messages_dict = [
        msg.model_dump() if isinstance(msg, ChatMessage) else msg for msg in messages
    ]

    response = ollama.chat(model=model, messages=messages_dict)
    ai_response = response["message"]["content"]

    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    messages_dict.append({"role": "assistant", "content": ai_response})

    if chat_message:
        chats_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"messages": messages_dict}},
        )
    else:
        chats_collection.insert_one(
            {
                "user_id": user_id,
                "chat_id": generate_id(),  # this will must generate a new chat_id
                "messages": messages_dict,
                "model": model,
            }
        )

    return {"chat_id": str(chat_id), "response": ai_response}


def get_chat_section(user_id: str, chat_id: str) -> ChatSection:
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    if chat_message:
        return chat_message
    else:
        raise HTTPException(status_code=404, detail="Chat not found")
