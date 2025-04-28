import asyncio
import logging
from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends, WebSocket, WebSocketDisconnect, status

from app.services.chat_service import (
    create_chat_completion,
    create_chat_completion_stream,
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
from app.middlewares.auth import get_current_user, get_current_user_optional, get_current_user_ws


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("/ws")
async def chat_stream(
    *,
    websocket: WebSocket,
    user: Annotated[Optional[dict], Depends(get_current_user_ws)]
):
    """
    WebSocket endpoint for real-time chat streaming with Ollama AI.

    This endpoint allows clients to establish a WebSocket connection for interactive chat sessions.
    The client may optionally authenticate by providing a JWT token (as a query parameter or header).
    Once connected, the server will send a `{"status": "connected"}` message.

    **Receiving Data:**
    - The server expects JSON messages from the client with at least a `command` field.
    - Supported commands:
        - `"chat"` (default): Start a new AI response generation. The message should include:
            - `messages`: List of chat messages (history + new user message).
            - `model` (optional): Model name to use.
            - `chat_id` (optional): Chat session identifier.
        - `"interrupt"`: Interrupt the current AI response generation.

    **Response Data:**
    - On connection: `{"status": "connected"}`
    - On `"chat"` command:
        - Streaming responses: `{"status": "streaming", "chunk": ...}` (multiple times)
        - On completion: `{"status": "complete", "message": ...}`
        - On error: `{"status": "error", "message": ...}`
    - On `"interrupt"` command:
        - `{"status": "interrupted", "content": ...}`

    The server handles only one active generation task per connection. If interrupted, the current task is cancelled.
    On disconnect, any running generation task is also cancelled.
    """
    await websocket.accept()
    user_id = user.get("user_id") if user else None
    logging.info(f"WebSocket connected for user: {user_id}")
    current_generation_task = None

    try:
        await websocket.send_json({"status": "connected", "message": "WebSocket connected for user: " + str(user_id)})

        while True:
            data = await websocket.receive_json()
            command = data.get("command", "chat")

            logging.info(f"Received command: {command} {data}")
            
            if command == "interrupt":
                if current_generation_task and not current_generation_task.done():
                    current_generation_task.cancel()
                    await websocket.send_json({
                        "status": "interrupted",
                        "content": "Response generation interrupted"
                    })
                continue
    
            messages = data.get("messages", [])
            model = data.get("model", settings.DEFAULT_MODEL)
            chat_id = data.get("chat_id")
            
            current_generation_task = asyncio.create_task(
                create_chat_completion_stream(websocket, user_id, chat_id, messages, model)
            )
            
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
        if current_generation_task and not current_generation_task.done():
            current_generation_task.cancel()
    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})


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
    "/models",
    response_model=AvailableModelsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all models",
    description="Retrieve a list of all available models from the Ollama service",
)
def get_models(user: dict = Depends(get_current_user)):
    return get_available_models()


@router.get(
    "/{chat_id}",
    response_model=ChatConversation,
    status_code=status.HTTP_200_OK,
    summary="Get chat section",
    description="Get chat section by chat_id for the current user",
)
def get_chat(chat_id: str, user: dict = Depends(get_current_user)):
    return get_chat_conversation(user["user_id"], chat_id)


@router.get(
    "/",
    response_model=UserChatsCollection,
    status_code=status.HTTP_200_OK,
    summary="Get all user chats",
    description="Retrieve a list of all chat sessions for the current user",
)
def list_chats(user: dict = Depends(get_current_user)):
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
    user: dict = Depends(get_current_user),
):
    return rename_chat_conversation(user["user_id"], chat_id, chat_title)


@router.delete(
    "/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete chat section",
    description="Delete a chat section by chat_id for the current user",
)
def delete_chat(chat_id: str, user: dict = Depends(get_current_user)):
    return delete_chat_conversation(user["user_id"], chat_id)
