from typing import List
from fastapi import HTTPException, status

from app.database import chats_collection
from app.models.chat import (
    ChatMessage, ChatCompletionResponse, ChatConversation,
    ChatRenameResponse, UserChatsCollection, AIModel, AvailableModelsResponse
)
from app.utils import generate_id, get_current_time, format_size
from app.config import settings
from app.services.ollama_service import send_chat_to_ollama, generate_chat_title, get_all_ollama_models


def create_chat_completion(user_id: str, chat_id: str, messages: List[ChatMessage], model: str = settings.DEFAULT_MODEL) -> ChatCompletionResponse:
    messages_dict = [msg.model_dump() if isinstance(msg, ChatMessage) else msg for msg in messages]

    if messages_dict[-1]["role"] != "user":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from the user",
        )

    ai_response = send_chat_to_ollama(messages)

    messages_dict.append({"role": "assistant", "content": ai_response})

    if user_id:
        chat_id = generate_id() if not chat_id and user_id else chat_id
        chat_title = generate_chat_title(messages_dict)
        save_chat_conversation(messages_dict, user_id, chat_id, model, chat_title)
        return ChatCompletionResponse(chat_id=str(chat_id), title=chat_title, response=ai_response)

    return ChatCompletionResponse(response=ai_response)


def save_chat_conversation(messages_dict: List[ChatMessage], user_id: str, chat_id: str, model: str, chat_title: str = None):
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})

    if chat_message:
        chats_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"messages": messages_dict, "title": chat_title or chat_message["title"]}},
        )
    else:
        chat_id = generate_id()
        chats_collection.insert_one(
            ChatConversation(
                user_id=user_id,
                chat_id=chat_id,
                title=chat_title or "Untitled",
                created_at=get_current_time(),
                model=model,
                messages=messages_dict,
            ).model_dump()
        )


def rename_chat_conversation(user_id: str, chat_id: str, title: str) -> ChatRenameResponse:
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})
    if chat_message:
        chats_collection.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {"$set": {"title": title}},
        )
        return ChatRenameResponse(chat_id=chat_id, title=title, success=True)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Chat section '{chat_id}' not found for user '{user_id}'",
    )


def get_user_chats_collection(user_id: str) -> UserChatsCollection:
    chats_in_db = list(chats_collection.find({"user_id": user_id}, {"messages": 0}).sort("created_at", -1))
    chat_sections = []
    for chat in chats_in_db:
        chat["_id"] = str(chat["_id"])
        if not isinstance(chat["created_at"], str):
            chat["created_at"] = chat["created_at"].strftime("%Y-%m-%dT%H:%M:%SZ")
        chat["messages"] = []
        chat_sections.append(ChatConversation.model_validate(chat))

    return UserChatsCollection(user_id=user_id, chats=chat_sections)


def get_chat_conversation(user_id: str, chat_id: str) -> ChatConversation:
    chat_message = chats_collection.find_one({"user_id": user_id, "chat_id": chat_id})
    if chat_message:
        return ChatConversation.model_validate(chat_message)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Chat section '{chat_id}' not found for user '{user_id}'",
    )


def delete_chat_conversation(user_id: str, chat_id: str) -> bool:
    result = chats_collection.delete_one({"user_id": user_id, "chat_id": chat_id})
    if result.deleted_count == 1:
        return True
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Chat section '{chat_id}' not found for user '{user_id}'",
    )


def get_available_models() -> AvailableModelsResponse:
    models = get_all_ollama_models()
    model_data = [AIModel(name=model.model, size=format_size(model.size)) for model in models]
    return AvailableModelsResponse(models=model_data, total=len(model_data))
