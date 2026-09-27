"""Colibri inference adapter for Gungv-Nexus.

Nexus owns orchestration, memory, safety and provider selection. Colibri is
treated as an optional inference backend exposing an OpenAI-compatible API.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ColibriConfig:
    base_url: str = "http://127.0.0.1:8080"
    model: str = "auto"
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "ColibriConfig":
        return cls(
            base_url=os.getenv("NEXUS_COLIBRI_BASE_URL", cls.base_url).rstrip("/"),
            model=os.getenv("NEXUS_COLIBRI_MODEL", cls.model),
            timeout=float(os.getenv("NEXUS_COLIBRI_TIMEOUT", str(cls.timeout))),
        )


class ColibriAdapter:
    """Thin, dependency-free adapter around a Colibri `coli serve` endpoint."""

    capability = "large-model-inference"
    repository = "JustVugg/colibri"

    def __init__(self, config: ColibriConfig | None = None):
        self.config = config or ColibriConfig.from_env()

    def _request(self, path: str, payload: dict[str, Any] | None = None) -> Any:
        url = f"{self.config.base_url}{path}"
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST" if body is not None else "GET",
        )
        with urllib.request.urlopen(request, timeout=self.config.timeout) as response:
            raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}

    def health(self) -> dict[str, Any]:
        last_error = None
        for path in ("/health", "/v1/models"):
            try:
                data = self._request(path)
                return {
                    "available": True,
                    "endpoint": self.config.base_url,
                    "probe": path,
                    "response": data,
                }
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                last_error = str(exc)
        return {
            "available": False,
            "endpoint": self.config.base_url,
            "error": last_error,
        }

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model or self.config.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        return self._request("/v1/chat/completions", payload)

    def status(self) -> dict[str, Any]:
        return {
            "provider": "colibri",
            "repository": self.repository,
            "mode": "external-local-runtime",
            "endpoint": self.config.base_url,
            "model": self.config.model,
            "architecture": {
                "ssd": "model-storage/streaming",
                "ram": "resident-hot-state",
                "vram": "optional-acceleration",
                "cache": "provider-managed-expert-cache",
            },
            "health": self.health(),
        }
