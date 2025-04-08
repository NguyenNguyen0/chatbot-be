import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    DEFAULT_MODEL: str = "llama3"
    MONGO_URI: str = Field(..., env="MONGO_URI")
    ORIGINS: str = os.getenv("ORIGINS", "*")
    
    class Config:
        env_file = ".env"

settings = Settings()
