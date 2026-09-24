"""Provider-agnostic AI Live Host controller.

No secrets are stored here. The controller can run fully offline in demo mode.
"""
from __future__ import annotations

import os
import time
import uuid
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
        self.supporters[user or "anonymous"] = self.supporters.get(user or "anonymous", 0.0) + amount


class HostController:
    """Deterministic controller with optional external AI generation."""

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

    def respond(self, event: Event) -> str:
        """Return a safe deterministic response suitable for a first MVP."""
        if event.kind == "support":
            name = event.user or "teman"
            amount = f"{event.amount:g} {event.currency}" if event.amount is not None else "dukungan"
            response = f"Terima kasih {name} atas dukungannya sebesar {amount}. Kita lanjutkan live."
        elif event.text:
            text = event.text.strip()
            response = f"Terima kasih pertanyaannya. Saya akan membahas: {text}"
        else:
            response = "Halo semuanya. Silakan kirim pertanyaan di chat."

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
                "provider_mode": "optional-http" if os.getenv("OPENAI_API_KEY") else "deterministic",
            },
        }
