from typing import List
import logging
import ollama
from fastapi import HTTPException, status

from app.database import chats_collection
from app.models.chat import (
    BotModel,
    BotModelResponse,
    ChatMessage,
    ChatResponse,
    ChatSection,
    RenameResponse,
    UserChatList,
)
from app.utils import generate_id, get_current_time, format_size
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

    if messages_dict[-1]["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from the user",
        )

    try:
        response = ollama.chat(model=model, messages=messages_dict)
        ai_response = response["message"]["content"]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to communicate with Ollama service: {str(e)}",
        )

    messages_dict.append({"role": "assistant", "content": ai_response})
    chat_id = generate_id() if not chat_id and user_id else chat_id
    chat_title = naming_chat_section(user_id, chat_id, messages_dict)

    if user_id:
        save_chat_section(
            messages_dict=messages_dict,
            user_id=user_id,
            chat_id=chat_id,
            model=model,
            chat_title=chat_title,
        )


    return ChatResponse(chat_id=str(chat_id), title=chat_title, response=ai_response)


def save_chat_section(messages_dict: List[ChatMessage], user_id: str, chat_id: str, model: str, chat_title: str = None):
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    if chat_message:
        chats_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {
                "$set": {
                    "messages": messages_dict,
                    "title": chat_title if chat_title else chat_message["title"],
                }
            },
        )
    else:
        chat_id = generate_id()
        chats_collection.insert_one(
            ChatSection(
                user_id=user_id,
                chat_id=chat_id,
                title=chat_title if chat_title else "Untitled",
                created_at=get_current_time(),
                model=model,
                messages=messages_dict,
            ).model_dump()
        )


def naming_chat_section(user_id: str, chat_id: str, messages: List[ChatMessage]):
    messages_dict = [
        msg.model_dump() if isinstance(msg, ChatMessage) else msg for msg in messages
    ]

    if messages_dict[-1]["role"] != "assistant":
        logging.error("Last message must from bot", exc_info=True)
        return None

    messages_dict.append(
        {
            "role": "user",
            "content": "give a shortest title for this conversation under 8 words",
        }
    )

    if len(messages_dict) > 4:
        return None

    try:
        response = ollama.chat(model=settings.DEFAULT_MODEL, messages=messages_dict)
        ai_response = response["message"]["content"]
        return ai_response.replace('"', "")
    except Exception as e:
        logging.error(
            f"Failed to generate title for chat_id={chat_id}, user_id={user_id}: {str(e)}",
            exc_info=True,
        )
        return None


def rename_chat_section(user_id: str, chat_id: str, title: str) -> RenameResponse:
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    if chat_message:
        chats_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"title": title}},
        )
        return RenameResponse(chat_id=chat_id, title=title, success=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat section '{chat_id}' not found for user '{user_id}'",
        )


def get_all_models() -> BotModelResponse:
    try:
        response = ollama.list()
        models = [
            BotModel(name=model.model, size=format_size(model.size))
            for model in response.models
        ]
        return BotModelResponse(models=models, total=len(models))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch models from Ollama service: {str(e)}",
        )


def get_chat_section(user_id: str, chat_id: str) -> ChatSection:
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    if chat_message:
        return ChatSection.model_validate(chat_message)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat section '{chat_id}' not found for user '{user_id}'",
        )


def get_user_chats(user_id: str) -> UserChatList:
    chats_in_db = list(
        chats_collection.find({"user_id": user_id}, {"messages": 0}).sort(
            "created_at", -1
        )
    )
    chat_sections = []
    for chat in chats_in_db:
        chat["_id"] = str(chat["_id"])

        if not isinstance(chat["created_at"], str):
            chat["created_at"] = chat["created_at"].strftime("%Y-%m-%dT%H:%M:%SZ")

        chat["messages"] = []  # get only metadata, not messages

        chat_sections.append(ChatSection.model_validate(chat))

    return UserChatList(user_id=user_id, chats=chat_sections)


def delete_chat_section(user_id: str, chat_id: str) -> bool:
    result = chats_collection.delete_one({"user_id": user_id, "chat_id": chat_id})

    if result.deleted_count == 1:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat section '{chat_id}' not found for user '{user_id}'",
        )
