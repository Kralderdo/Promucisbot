from pyrogram import Client, enums
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.session import StringSession
from .config import settings

def build_assistant() -> Client:
    if settings.SESSION_STRING:
        return Client(
            name="prenses-assistant",
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            session_string=settings.SESSION_STRING,
            parse_mode=enums.ParseMode.HTML,
        )
    # Fallback: phone login (interactive, Heroku'da önerilmez)
    if settings.ASSISTANT_PHONE:
        return Client(
            name="prenses-assistant",
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            phone_number=settings.ASSISTANT_PHONE,
            parse_mode=enums.ParseMode.HTML,
        )
    raise RuntimeError("SESSION_STRING veya ASSISTANT_PHONE zorunlu!")

assistant = build_assistant()
