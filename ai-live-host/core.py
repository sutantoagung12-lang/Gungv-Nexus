"""Provider-agnostic AI Live Host controller.

The core can run offline. If OPENAI_API_KEY is configured, it can optionally
generate a response through the OpenAI Responses API. Secrets are read only
from environment variables and are never persisted by this module.
"""
from __future__ import annotations

import json
import os
import time
import uuid
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Event:
    kind: str
    text: str = ""
    user: str = ""
    amount: float | None = None
    currency: str = "IDR"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)


@dataclass
class SessionMemory:
    messages: list[dict[str, str]] = field(default_factory=list)
    supporters: dict[str, float] = field(default_factory=dict)

    def add(self, role: str, text: str) -> None:
        self.messages.append({"role": role, "text": text})
        if len(self.messages) > 40:
            del self.messages[:-40]

    def support(self, user: str, amount: float) -> None:
        key = user or "anonymous"
        self.supporters[key] = self.supporters.get(key, 0.0) + amount


class HostController:
    """Conversation controller with deterministic and optional AI modes."""

    def __init__(self) -> None:
        self.memory = SessionMemory()
        self.events: list[Event] = []
        self.started_at: float | None = None
        self.live = False
        self.dry_run = os.getenv("LIVE_DRY_RUN", "1").lower() not in {"0", "false", "no"}

    def start(self) -> dict[str, Any]:
        self.started_at = time.time()
        self.live = True
        return self.status()

    def stop(self) -> dict[str, Any]:
        self.live = False
        return self.status()

    def ingest(self, event: Event) -> None:
        self.events.append(event)
        if len(self.events) > 100:
            del self.events[:-100]
        if event.kind == "support" and event.amount is not None:
            self.memory.support(event.user, event.amount)
            self.memory.add("system", f"Support event from {event.user or 'anonymous'}: {event.amount:g} {event.currency}.")
        elif event.text:
            self.memory.add("user", event.text)

    def _deterministic(self, event: Event) -> str:
        if event.kind == "support":
            name = event.user or "teman"
            amount = f"{event.amount:g} {event.currency}" if event.amount is not None else "dukungan"
            return f"Terima kasih {name} atas dukungannya sebesar {amount}. Kita lanjutkan live."
        if event.text:
            return f"Terima kasih pertanyaannya. Saya akan membahas: {event.text.strip()}"
        return "Halo semuanya. Silakan kirim pertanyaan di chat."

    def _openai_response(self, event: Event) -> str | None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            return None
        model = os.getenv("OPENAI_MODEL")
        if not model:
            return None
        recent = self.memory.messages[-12:]
        instructions = (
            "Kamu adalah host live AI berbahasa Indonesia. Jawab singkat, natural, "
            "sopan, tidak membuat klaim palsu, dan jangan meminta data pribadi. "
            "Untuk event dukungan, ucapkan terima kasih tanpa menjanjikan imbalan."
        )
        payload = {
            "model": model,
            "instructions": instructions,
            "input": json.dumps({"event": event.__dict__, "recent_memory": recent}, ensure_ascii=False),
            "max_output_tokens": 180,
        }
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                data = json.loads(response.read().decode())
            text = data.get("output_text")
            return text.strip() if isinstance(text, str) and text.strip() else None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            return None

    def respond(self, event: Event) -> str:
        response = self._openai_response(event) or self._deterministic(event)
        self.memory.add("assistant", response)
        return response

    def status(self) -> dict[str, Any]:
        return {
            "service": "ai-live-host",
            "version": "0.1.0",
            "live": self.live,
            "dry_run": self.dry_run,
            "started_at": self.started_at,
            "events": len(self.events),
            "memory_messages": len(self.memory.messages),
            "supporters": len(self.memory.supporters),
            "youtube": {
                "access_token_configured": bool(os.getenv("YOUTUBE_ACCESS_TOKEN")),
                "chat_id_configured": bool(os.getenv("YOUTUBE_LIVE_CHAT_ID")),
            },
            "ai": {
                "openai_key_configured": bool(os.getenv("OPENAI_API_KEY")),
                "model_configured": bool(os.getenv("OPENAI_MODEL")),
                "provider_mode": "openai-http" if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_MODEL") else "deterministic",
            },
        }
