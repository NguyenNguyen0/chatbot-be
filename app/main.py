from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.logger import LoggingMiddleware
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.config import settings

app = FastAPI(
    title="Simple Chatbot API",
    description="A simple chatbot API using FastAPI and Ollama",
    version="0.1.0",
)

app.add_middleware(LoggingMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ORIGINS],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def read_root():
    return {"FastApi": "Hello World"}


app.include_router(chat_router)
app.include_router(auth_router)
