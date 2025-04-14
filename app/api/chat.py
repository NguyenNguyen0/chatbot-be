from fastapi import APIRouter, Depends, status

from app.services.ollama_service import chat_with_ollama, get_chat_section, get_user_chats, delete_chat_section, get_all_models
from app.models.chat import BotModelResponse, ChatRequest, ChatResponse, ChatSection, UserChatList
from app.config import settings
from app.middlewares.auth import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get(
    '/models',
    response_model=BotModelResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all models",
    description="Retrieve a list of all available models from the Ollama service"
)
def get_models():
    return get_all_models()


@router.post(
    "/",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Chat with Ollama",
    description="Chat with Ollama models to get AI responses"
)
def chat(
    chat_request: ChatRequest,
    user=Depends(get_current_user),
):
    messages = chat_request.messages
    model = chat_request.model if chat_request.model else settings.DEFAULT_MODEL
    chat_id = chat_request.chat_id if chat_request.chat_id else None
    return chat_with_ollama(user["user_id"], chat_id, messages, model)


@router.get(
    "/{chat_id}",
    response_model=ChatSection,
    status_code=status.HTTP_200_OK,
    summary="Get chat section",
    description="Get chat section by chat_id for the current user"
)
def get_chat(chat_id: str, user: str = Depends(get_current_user)):
    return get_chat_section(user["user_id"], chat_id)


@router.get(
    "/", 
    response_model=UserChatList,
    status_code=status.HTTP_200_OK,
    summary="Get all user chats",
    description="Retrieve a list of all chat sessions for the current user"
)
def list_chats(user=Depends(get_current_user)):
    return get_user_chats(user["user_id"])


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete chat section",
    description="Delete a chat section by chat_id for the current user"
)
def delete_chat(chat_id: str, user=Depends(get_current_user)):
    return delete_chat_section(user["user_id"], chat_id)