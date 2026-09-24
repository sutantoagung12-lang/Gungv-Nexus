"""Persistent bounded episodic experience with typed, quality-aware lessons."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Experience:
    task: str
    plan: list[dict] = field(default_factory=list)
    capabilities_used: list[str] = field(default_factory=list)
    result: str = "unknown"
    errors: list[str] = field(default_factory=list)
    quality: float = 0.0
    reward: float = 0.0
    lessons: list[str] = field(default_factory=list)
    lesson_records: list[dict] = field(default_factory=list)
    latency_ms: float | None = None
    cost: float | None = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExperienceStore:
    def __init__(self, max_items: int = 500, max_lessons: int = 500, path: str | None = None):
        self.max_items = max(1, max_items)
        self.max_lessons = max(1, max_lessons)
        self.path = Path(path) if path else None
        self._items: list[dict[str, Any]] = []
        self._lessons: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.path or not self.path.exists():
            return
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(item, dict) or not item.get("task"):
                continue
            self._items.append(item)
            for record in item.get("lesson_records", []):
                self._lessons.append({
                    **record,
                    "source_task": item["task"],
                    "reward": item.get("reward", 0.0),
                    "quality": item.get("quality", 0.0),
                    "timestamp": item.get("timestamp"),
                })
        self._items = self._items[-self.max_items:]
        self._lessons = self._lessons[-self.max_lessons:]

    def _persist(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in self._items),
            encoding="utf-8",
        )
        tmp.replace(self.path)

    def record(self, experience: Experience) -> dict:
        item = asdict(experience)
        if not item["lesson_records"] and item["lessons"]:
            item["lesson_records"] = [
                {"lesson": lesson, "type": "strategic",
                 "confidence": round((float(item["quality"]) + float(item["reward"])) / 2, 4),
                 "evidence_count": 1}
                for lesson in item["lessons"]
            ]
        if item["lesson_records"]:
            item["confidence"] = max(
                float(record.get("confidence", 0.0))
                for record in item["lesson_records"]
            )
            item["evidence_count"] = max(
                int(record.get("evidence_count", 1))
                for record in item["lesson_records"]
            )
        self._items.append(item)
        self._items = self._items[-self.max_items:]
        for record in item["lesson_records"]:
            self._lessons.append({
                **record, "source_task": item["task"],
                "reward": item["reward"], "quality": item["quality"],
                "timestamp": item["timestamp"],
            })
        self._lessons = self._lessons[-self.max_lessons:]
        self._persist()
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
        scored.sort(key=lambda x: (-x[0], -float(x[1].get("reward", 0.0)),
                                   -float(x[1].get("quality", 0.0))))
        return [item for _, item in scored[:max(1, limit)]]

    def lessons_for(self, task: str, limit: int = 5) -> list[dict]:
        tokens = set(task.lower().split())
        scored = []
        for item in self._lessons:
            overlap = len(tokens & set(item["lesson"].lower().split()))
            if overlap:
                scored.append((overlap, item))
        scored.sort(key=lambda x: (-x[0], -float(x[1].get("reward", 0.0)),
                                   -float(x[1].get("confidence", 0.0)),
                                   -int(x[1].get("evidence_count", 1))))
        return [item for _, item in scored[:max(1, limit)]]
