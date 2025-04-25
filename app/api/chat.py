from typing import Optional
from fastapi import APIRouter, Body, Depends, status

from app.services.chat_service import (
    create_chat_completion,
    get_chat_conversation,
    get_user_chats_collection,
    delete_chat_conversation,
    get_available_models,
    rename_chat_conversation,
)
from app.models.chat import (
    AvailableModelsResponse,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatConversation,
    UserChatsCollection,
    ChatRenameResponse,
)
from app.config import settings
from app.middlewares.auth import get_current_user, get_current_user_optional

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get(
    "/models",
    response_model=AvailableModelsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all models",
    description="Retrieve a list of all available models from the Ollama service",
)
def get_models():
    return get_available_models()


@router.post(
    "/",
    response_model=ChatCompletionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Chat with Ollama",
    description="Chat with Ollama models to get AI responses. If authenticated, the chat history will be saved to the user's account.",
)
def chat(
    chat_request: ChatCompletionRequest,
    user: Optional[dict] = Depends(get_current_user_optional),
):
    messages = chat_request.messages
    model = chat_request.model if chat_request.model else settings.DEFAULT_MODEL
    chat_id = chat_request.chat_id if chat_request.chat_id else None
    
    user_id = user["user_id"] if user else None
    return create_chat_completion(user_id, chat_id, messages, model)


@router.get(
    "/{chat_id}",
    response_model=ChatConversation,
    status_code=status.HTTP_200_OK,
    summary="Get chat section",
    description="Get chat section by chat_id for the current user",
)
def get_chat(chat_id: str, user: str = Depends(get_current_user)):
    return get_chat_conversation(user["user_id"], chat_id)


@router.get(
    "/",
    response_model=UserChatsCollection,
    status_code=status.HTTP_200_OK,
    summary="Get all user chats",
    description="Retrieve a list of all chat sessions for the current user",
)
def list_chats(user=Depends(get_current_user)):
    return get_user_chats_collection(user["user_id"])


@router.patch(
    "/{chat_id}",
    response_model=ChatRenameResponse,
    status_code=status.HTTP_200_OK,
    summary="Rename chat title",
    description="Rename the title of a chat section by chat_id for the current user",
)
def rename_chat(
    chat_id: str,
    chat_title: str = Body(..., description="New chat title", example="My New Chat"),
    user=Depends(get_current_user),
):
    return rename_chat_conversation(user["user_id"], chat_id, chat_title)


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete chat section",
    description="Delete a chat section by chat_id for the current user",
)
def delete_chat(chat_id: str, user=Depends(get_current_user)):
    return delete_chat_conversation(user["user_id"], chat_id)
