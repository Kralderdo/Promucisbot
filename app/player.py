from __future__ import annotations
import asyncio
from collections import deque
from typing import Deque, Dict, Optional

from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types.input_stream import AudioPiped, InputStream
from pytgcalls.types.playlist import InputAudioStream
from pytgcalls.types.stream import StreamAudioEnded

from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired

from .assistant import assistant
from .yt import yt_search

import yt_dlp

class Track:
    def __init__(self, title: str, url: str, requested_by: str):
        self.title = title
        self.url = url
        self.requested_by = requested_by

class Player:
    def __init__(self):
        self.app = assistant
        self.tgcalls = PyTgCalls(self.app)
        self.queues: Dict[int, Deque[Track]] = {}
        self.lock: Dict[int, asyncio.Lock] = {}

    async def start(self):
        await self.app.start()
        await self.tgcalls.start()

    async def stop(self):
        await self.tgcalls.stop()
        await self.app.stop()

    def get_queue(self, chat_id: int) -> Deque[Track]:
        if chat_id not in self.queues:
            self.queues[chat_id] = deque()
        if chat_id not in self.lock:
            self.lock[chat_id] = asyncio.Lock()
        return self.queues[chat_id]

    async def _yt_to_audio(self, url: str) -> str:
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "noplaylist": True,
            "extractaudio": True,
            "outtmpl": f"/tmp/%(id)s.%(ext)s",
            "cachedir": False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"]  # direct stream URL

    async def join_if_needed(self, chat_id: int):
        if self.tgcalls.get_call(chat_id):
            return
        # İlk parça gelince otomatik bağlanır; burada dummy bağlanma yok.

    async def enqueue(self, m: Message, query_or_url: str):
        chat_id = m.chat.id
        q = self.get_queue(chat_id)

        # Arama gerekiyorsa
        if query_or_url.startswith("http"):
            url = query_or_url
            title = query_or_url
        else:
            results = yt_search(query_or_url, max_results=1)
            if not results:
                await m.reply_text("YouTube'da sonuç bulunamadı.")
                return
            url = results[0]["url"]
            title = results[0]["title"]

        q.append(Track(title=title, url=url, requested_by=m.from_user.mention if m.from_user else "Bir kullanıcı"))
        await m.reply_text(f"🎧 Sıraya eklendi: <b>{title}</b>")

        # Eğer şu an çalmıyorsa başlat
        if len(q) == 1:
            await self._play_next(chat_id, m)

    async def _play_next(self, chat_id: int, m: Optional[Message] = None):
        q = self.get_queue(chat_id)
        if not q:
            # Boşsa ayrıl
            try:
                await self.tgcalls.leave_group_call(chat_id)
            except Exception:
                pass
            return

        track = q[0]
        try:
            stream_url = await self._yt_to_audio(track.url)
            await self.tgcalls.join_group_call(
                chat_id,
                InputStream(
                    AudioPiped(stream_url),
                ),
                stream_type=0,
            )
            if m:
                await m.reply_text(f"▶️ Çalıyor: <b>{track.title}</b>")
        except ChatAdminRequired:
            if m:
                await m.reply_text("Sesli sohbete bağlanamıyorum. Asistanı sunucu yöneticisi yapın ve sesli sohbet açın.")
        except Exception as e:
            if m:
                await m.reply_text(f"Çalma hatası: <code>{e}</code>")
            # Parçayı atla ve devam et
            if q:
                q.popleft()
            await self._play_next(chat_id, m)

    async def skip(self, chat_id: int, m: Optional[Message] = None):
        q = self.get_queue(chat_id)
        if q:
            q.popleft()
        try:
            await self.tgcalls.leave_group_call(chat_id)
        except Exception:
            pass
        await self._play_next(chat_id, m)

    async def pause(self, chat_id: int):
        if self.tgcalls.get_call(chat_id):
            await self.tgcalls.pause_stream(chat_id)

    async def resume(self, chat_id: int):
        if self.tgcalls.get_call(chat_id):
            await self.tgcalls.resume_stream(chat_id)

    async def stop_all(self, chat_id: int):
        self.queues[chat_id] = deque()
        try:
            await self.tgcalls.leave_group_call(chat_id)
        except Exception:
            pass

player = Player()
