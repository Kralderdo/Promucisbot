from pyrogram import filters
from pyrogram.types import Message
from ..bot import bot

@bot.on_message(filters.command(["start","help"]) & filters.private)
async def start_private(_, m: Message):
    await m.reply_text(
        "🎵 <b>Prenses Music Bot</b>\n"
        "Komutlar:\n"
        "/play <şarkı> – Sıraya ekle ve çal\n"
        "/skip – Geç\n"
        "/pause – Duraklat\n"
        "/resume – Devam\n"
        "/stop – Durdur\n"
        "/queue – Sırayı göster"
    )
