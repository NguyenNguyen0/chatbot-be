import ollama
from app.database import chats_collection


def chat_with_ollama(user_id: str, message: str, model: str = "mistral"):
    response = ollama.chat(model=model, messages=[{"role": "user", "content": message}])
    ai_response = response["message"]["content"]

    chat_id = chats_collection.insert_one(
        {"user_id": user_id, "message": message, "response": ai_response}
    ).inserted_id

    return {"chat_id": str(chat_id), "response": ai_response}
