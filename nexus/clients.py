from __future__ import annotations

import os
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class ServiceClient:
    base_url: str
    token: str | None = None

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def health(self) -> dict:
        response = httpx.get(f"{self.base_url.rstrip('/')}/health", headers=self._headers(), timeout=10)
        response.raise_for_status()
        return response.json()


def cmra_client() -> ServiceClient | None:
    url = os.getenv("CMRA_URL")
    return ServiceClient(url, os.getenv("CMRA_TOKEN")) if url else None


def workers_client() -> ServiceClient | None:
    url = os.getenv("WORKERS_URL")
    return ServiceClient(url, os.getenv("WORKERS_TOKEN")) if url else None


def automation_client() -> ServiceClient | None:
    url = os.getenv("AUTOMATION_URL")
    return ServiceClient(url, os.getenv("AUTOMATION_TOKEN")) if url else None
