"""Persistent, quality-gated skill memory for Nexus v26."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


@dataclass
class Skill:
    skill_id: str
    name: str
    description: str
    procedure: str
    source_lessons: list[str] = field(default_factory=list)
    evidence_count: int = 0
    quality: float = 0.0
    reward: float = 0.0
    confidence: float = 0.0
    status: str = "ACTIVE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SkillStore:
    def __init__(self, path: str, max_items: int = 500):
        self.path = Path(path)
        self.max_items = max(1, max_items)
        self._items: list[dict[str, Any]] = []
        self._load()

    @staticmethod
    def stable_id(lesson: str) -> str:
        return sha256(lesson.strip().lower().encode("utf-8")).hexdigest()[:16]

    def _load(self) -> None:
        if not self.path.exists():
            return
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
                if isinstance(item, dict) and item.get("skill_id"):
                    self._items.append(item)
            except json.JSONDecodeError:
                continue
        self._items = self._items[-self.max_items:]

    def _persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in self._items),
            encoding="utf-8",
        )
        tmp.replace(self.path)

    def upsert(self, skill: Skill) -> dict:
        item = asdict(skill)
        for index, current in enumerate(self._items):
            if current.get("skill_id") == skill.skill_id:
                merged = {**current, **item}
                merged["source_lessons"] = sorted(set(
                    current.get("source_lessons", []) + skill.source_lessons
                ))
                merged["evidence_count"] = max(
                    int(current.get("evidence_count", 0)), skill.evidence_count
                )
                merged["updated_at"] = datetime.now(timezone.utc).isoformat()
                self._items[index] = merged
                self._persist()
                return merged
        self._items.append(item)
        self._items = self._items[-self.max_items:]
        self._persist()
        return item

    def all(self) -> list[dict]:
        return list(self._items)

    def search(self, task: str, limit: int = 5) -> list[dict]:
        query = set(task.lower().split())
        ranked = []
        for item in self._items:
            tokens = set((item.get("name", "") + " " + item.get("description", "")).lower().split())
            overlap = len(query & tokens)
            if overlap:
                score = overlap / max(1, len(query | tokens))
                ranked.append((score, item))
        ranked.sort(key=lambda pair: (-pair[0], -float(pair[1].get("quality", 0.0)),
                                     -int(pair[1].get("evidence_count", 0))))
        return [{**item, "skill_score": round(score, 4)}
                for score, item in ranked[:max(1, limit)]]
