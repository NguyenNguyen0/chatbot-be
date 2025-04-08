from typing import List
import ollama
from fastapi import HTTPException, status

from app.database import chats_collection
from app.models.chat import ChatMessage, ChatResponse, ChatSection, UserChatList
from app.utils import generate_id, get_current_time
from app.config import settings


def chat_with_ollama(
    user_id: str,
    chat_id: str,
    messages: List[ChatMessage],
    model: str = settings.DEFAULT_MODEL,
) -> ChatResponse:
    messages_dict = [
        msg.model_dump() if isinstance(msg, ChatMessage) else msg for msg in messages
    ]

    if messages_dict[-1]['role'] != "user":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Last message must be from the user")

    try:
        response = ollama.chat(model=model, messages=messages_dict)
        ai_response = response["message"]["content"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"Failed to communicate with Ollama service: {str(e)}"
        )

    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    messages_dict.append({"role": "assistant", "content": ai_response})

    if chat_message:
        chats_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"messages": messages_dict, "title": messages_dict[0]["content"]}},
        )
    else:
        chat_id = generate_id()
        chats_collection.insert_one(
            ChatSection(
                user_id=user_id,
                chat_id=chat_id,
                title=messages_dict[0]["content"],
                created_at=get_current_time(),
                model=model,
                messages=messages_dict,
            ).model_dump()
        )

    return ChatResponse(chat_id=str(chat_id), response=ai_response)


def get_chat_section(user_id: str, chat_id: str) -> ChatSection:
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    if chat_message:
        return ChatSection.model_validate(chat_message)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Chat section '{chat_id}' not found for user '{user_id}'")


def get_user_chats(user_id: str) -> UserChatList:
    chats_in_db = list(chats_collection.find({"user_id": user_id}, {"messages": 0}).sort("created_at", -1))
    chat_sections = []
    for chat in chats_in_db:
        chat["_id"] = str(chat["_id"])

        if not isinstance(chat["created_at"], str):
            chat["created_at"] = chat["created_at"].strftime("%Y-%m-%dT%H:%M:%SZ")

        chat["messages"] = [] # get only metadata, not messages

        chat_sections.append(ChatSection.model_validate(chat))

    return UserChatList(user_id=user_id, chats=chat_sections)