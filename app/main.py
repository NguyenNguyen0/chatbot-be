from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

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
def read_root() -> RedirectResponse:
    """Render the root page."""
    with open("app/html/index.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.get("/ws", tags=["Test"])
def test_ws():
    """Serve the WebSocket UI test page."""
    with open("app/html/test_websocket.html", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


app.include_router(chat_router)
app.include_router(auth_router)
