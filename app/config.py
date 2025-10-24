import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    SESSION_STRING: str | None = os.getenv("SESSION_STRING")
    ASSISTANT_PHONE: str | None = os.getenv("ASSISTANT_PHONE")
    LOG_GROUP_ID: int = int(os.getenv("LOG_GROUP_ID", "0"))
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")

settings = Settings()
