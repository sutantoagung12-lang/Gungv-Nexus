"""Minimal YouTube Live chat adapter using the official REST API.

The adapter sends messages to an already-created live chat. Stream creation,
OAuth consent, and token storage are intentionally outside this MVP.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request


class YouTubeError(RuntimeError):
    pass


class YouTubeLive:
    BASE = "https://www.googleapis.com/youtube/v3"

    def __init__(self, access_token: str | None = None, chat_id: str | None = None):
        self.access_token = access_token or os.getenv("YOUTUBE_ACCESS_TOKEN")
        self.chat_id = chat_id or os.getenv("YOUTUBE_LIVE_CHAT_ID")

    @property
    def configured(self) -> bool:
        return bool(self.access_token and self.chat_id)

    def send_chat(self, message: str) -> dict:
        if not self.configured:
            raise YouTubeError("YOUTUBE_ACCESS_TOKEN and YOUTUBE_LIVE_CHAT_ID are required.")
        payload = {
            "snippet": {
                "liveChatId": self.chat_id,
                "type": "textMessageEvent",
                "textMessageDetails": {"messageText": message},
            }
        }
        body = json.dumps(payload).encode()
        request = urllib.request.Request(
            self.BASE + "/liveChat/messages?part=snippet",
            data=body,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise YouTubeError(f"YouTube API HTTP {exc.code}: {detail[:500]}") from exc
        except urllib.error.URLError as exc:
            raise YouTubeError(f"YouTube API connection failed: {exc}") from exc
