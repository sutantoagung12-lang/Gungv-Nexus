"""Experience-aware retrieval for Nexus v25.

Ranks prior cases using lexical similarity plus outcome quality, reward,
confidence, recency, and lesson evidence. It is intentionally dependency-free
so the cognitive kernel remains lightweight and deterministic.
"""
from __future__ import annotations

from datetime import datetime, timezone
import math
import re
from typing import Any


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_]+", (text or "").lower()))


def _recency(timestamp: str) -> float:
    try:
        then = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        age_days = max(0.0, (datetime.now(timezone.utc) - then).total_seconds() / 86400)
        return math.exp(-age_days / 30.0)
    except (TypeError, ValueError):
        return 0.5


class ExperienceRetriever:
    """Retrieve useful prior cases without requiring an embedding service."""

    def __init__(self, store):
        self.store = store

    def rank(self, task: str, limit: int = 5) -> list[dict[str, Any]]:
        query = _tokens(task)
        if not query:
            return []

        ranked = []
        for item in self.store.recent(self.store.max_items):
            case_tokens = _tokens(item.get("task", ""))
            if not case_tokens:
                continue
            overlap = len(query & case_tokens)
            lexical = overlap / max(1, len(query | case_tokens))
            quality = max(0.0, min(1.0, float(item.get("quality", 0.0))))
            reward = max(0.0, min(1.0, float(item.get("reward", 0.0))))
            confidence = max(0.0, min(1.0, float(item.get("confidence", 0.0))))
            evidence = min(1.0, float(item.get("evidence_count", 1)) / 5.0)
            recency = _recency(item.get("timestamp", ""))
            score = (
                0.45 * lexical
                + 0.20 * quality
                + 0.15 * reward
                + 0.10 * confidence
                + 0.05 * evidence
                + 0.05 * recency
            )
            if overlap:
                ranked.append((score, item))

        ranked.sort(key=lambda pair: pair[0], reverse=True)
        return [
            {**item, "retrieval_score": round(score, 4)}
            for score, item in ranked[: max(1, limit)]
        ]

    def lessons(self, task: str, limit: int = 5) -> list[dict[str, Any]]:
        cases = self.rank(task, limit=max(limit * 2, 5))
        lessons = []
        seen = set()
        for case in cases:
            for lesson in case.get("lesson_records", []):
                text = lesson.get("lesson", "").strip()
                if text and text not in seen:
                    seen.add(text)
                    lessons.append({**lesson, "retrieval_score": case["retrieval_score"]})
                    if len(lessons) >= limit:
                        return lessons
        return lessons
