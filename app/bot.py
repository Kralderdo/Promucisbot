from pyrogram import Client, enums
from .config import settings

bot = Client(
    name="prenses-bot",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    bot_token=settings.BOT_TOKEN,
    in_memory=True,
    parse_mode=enums.ParseMode.HTML,
)
