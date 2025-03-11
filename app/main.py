from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router


app = FastAPI()


@app.get("/", tags=["Root"])
def read_root():
    return {"FastApi": "Hello World"}


app.include_router(chat_router)
app.include_router(auth_router)
