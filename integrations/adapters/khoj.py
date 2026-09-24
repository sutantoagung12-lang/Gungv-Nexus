"""Khoj memory/retrieval adapter boundary for Nexus."""

from typing import Any


class KhojAdapter:
    name = "Khoj"

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def status(self) -> dict[str, Any]:
        try:
            import khoj  # type: ignore
        except ImportError:
            return {"name": self.name, "available": False, "active": False}
        return {
            "name": self.name,
            "available": True,
            "active": bool(self.enabled),
            "version": getattr(khoj, "__version__", "unknown"),
        }

    def search_request(self, query: str, limit: int = 10) -> dict[str, Any]:
        if not query.strip():
            raise ValueError("query must not be empty")
        if limit < 1:
            raise ValueError("limit must be >= 1")
        return {
            "adapter": self.name,
            "query": query,
            "limit": limit,
            "execution_owner": "Gungv-Nexus",
        }
