"""Structured, bounded experience records for learning from task outcomes."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Experience:
    task: str
    plan: list[dict] = field(default_factory=list)
    capabilities_used: list[str] = field(default_factory=list)
    result: str = "unknown"
    errors: list[str] = field(default_factory=list)
    quality: float = 0.0
    latency_ms: float | None = None
    cost: float | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExperienceStore:
    def __init__(self, max_items: int = 500):
        self.max_items = max(1, max_items)
        self._items: list[dict[str, Any]] = []

    def record(self, experience: Experience) -> dict:
        item = asdict(experience)
        self._items.append(item)
        self._items = self._items[-self.max_items:]
        return item

    def recent(self, limit: int = 10) -> list[dict]:
        return self._items[-max(1, limit):]

    def similar(self, task: str, limit: int = 5) -> list[dict]:
        tokens = set(task.lower().split())
        scored = []
        for item in self._items:
            overlap = len(tokens & set(item["task"].lower().split()))
            if overlap:
                scored.append((overlap, item))
        scored.sort(key=lambda x: -x[0])
        return [item for _, item in scored[:max(1, limit)]]
