"""Adaptive capability resolver with runtime readiness and safe fallback."""
from __future__ import annotations

from integrations.capability_graph import build_graph
from integrations.capability_health import rank


def _matches(task: str, capability: str) -> int:
    text = task.lower()
    return sum(token in text for token in capability.replace("-", " ").replace("/", " ").split())


def resolve(task: str, limit: int = 5, runtime: dict | None = None, telemetry: dict | None = None, lessons: list[dict] | None = None) -> list[dict]:
    graph = build_graph(runtime)
    candidates = []
    lesson_text = " ".join(x.get("lesson", "") for x in (lessons or [])).lower()
    for capability, providers in graph.items():
        match = _matches(task, capability)
        if lesson_text and capability.replace("-", " ") in lesson_text:
            match += 1
        ready = rank([p for p in providers if p["readiness"] == "ready"], telemetry)
        if match and ready:
            candidates.append((match, capability, ready))
    candidates.sort(key=lambda x: (-x[0], -x[2][0]["health_score"], x[1]))
    return [{"capability": c, "providers": p[:limit], "fallback_count": max(0, len(p) - 1)} for _, c, p in candidates]
