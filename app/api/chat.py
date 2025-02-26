from fastapi import APIRouter, Depends
from app.services.ollama_service import chat_with_ollama

router = APIRouter()


@router.post("/")
def chat(user_id: str, message: str, model: str = "llama3"):
    return chat_with_ollama(user_id, message, model)
