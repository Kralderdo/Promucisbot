from pyrogram import filters
from pyrogram.types import Message
from ..bot import bot
from ..player import player

@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, m: Message):
    if len(m.command) < 2 and not (m.reply_to_message and (m.reply_to_message.text or m.reply_to_message.caption)):
        return await m.reply_text("Kullanım: /play <şarkı adı veya YouTube linki>")
    query = " ".join(m.command[1:]) if len(m.command) > 1 else (m.reply_to_message.text or m.reply_to_message.caption)
    await player.enqueue(m, query)

@bot.on_message(filters.command("skip") & filters.group)
async def skip_cmd(_, m: Message):
    await player.skip(m.chat.id, m)

@bot.on_message(filters.command("pause") & filters.group)
async def pause_cmd(_, m: Message):
    await player.pause(m.chat.id)
    await m.reply_text("⏸ Duraklatıldı.")

@bot.on_message(filters.command("resume") & filters.group)
async def resume_cmd(_, m: Message):
    await player.resume(m.chat.id)
    await m.reply_text("▶️ Devam.")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, m: Message):
    await player.stop_all(m.chat.id)
    await m.reply_text("⏹ Durduruldu ve ayrıldım.")

@bot.on_message(filters.command("queue") & filters.group)
async def queue_cmd(_, m: Message):
    q = player.get_queue(m.chat.id)
    if not q:
        return await m.reply_text("Sıra boş.")
    txt = "\n".join([f"{i+1}. <b>{t.title}</b> — {t.requested_by}" for i, t in enumerate(list(q))])
    await m.reply_text("🎼 <b>Sıra</b>\n" + txt)

@bot.on_message(filters.command("join") & filters.group)
async def join_cmd(_, m: Message):
    await player.join_if_needed(m.chat.id)
    await m.reply_text("Sesli sohbete bağlanmayı deneyeceğim. İlk /play ile otomatik bağlanırım.")
