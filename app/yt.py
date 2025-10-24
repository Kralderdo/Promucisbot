from __future__ import annotations
from googleapiclient.discovery import build
from .config import settings

def yt_search(query: str, max_results: int = 1) -> list[dict]:
    service = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)
    resp = service.search().list(q=query, part="id,snippet", maxResults=max_results, type="video").execute()
    items = []
    for it in resp.get("items", []):
        vid = it["id"]["videoId"]
        title = it["snippet"]["title"]
        items.append({"video_id": vid, "title": title, "url": f"https://www.youtube.com/watch?v={vid}"})
    return items
