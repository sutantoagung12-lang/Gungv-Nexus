"""Runtime-aware selection of autonomous skill patterns.

External skill repositories remain reference sources until independently validated.
This module selects operating patterns; it does not execute external code.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parent / "autonomous_skill_registry.json"

DEFAULT_PHASES = {
    "research": ["DISCOVER", "RETRIEVE", "PLAN", "VERIFY", "LEARN"],
    "search": ["DISCOVER", "RETRIEVE", "PLAN", "VERIFY"],
    "code": ["PLAN", "EXECUTE", "CHECKPOINT", "VERIFY", "RECOVER"],
    "build": ["PLAN", "EXECUTE", "CHECKPOINT", "VERIFY", "RECOVER"],
    "bug": ["RETRIEVE", "PLAN", "EXECUTE", "OBSERVE", "VERIFY", "RECOVER"],
    "debug": ["RETRIEVE", "PLAN", "EXECUTE", "OBSERVE", "VERIFY", "RECOVER"],
    "autonomous": ["DISCOVER", "RETRIEVE", "PLAN", "POLICY_CHECK", "EXECUTE",
                   "CHECKPOINT", "OBSERVE", "VERIFY", "RECOVER", "LEARN", "EVOLVE"],
    "evolve": ["EVALUATE", "VERIFY", "ACTIVATE"],
}


def load_registry() -> dict[str, Any]:
    with REGISTRY.open(encoding="utf-8") as fh:
        return json.load(fh)


def _tokens(text: str) -> set[str]:
    return {x for x in text.lower().replace("-", " ").split() if len(x) > 2}


def resolve_autonomous_skills(task: str, limit: int = 5) -> list[dict]:
    registry = load_registry()
    query = _tokens(task)
    phases = set()
    lowered = task.lower()
    for keyword, mapped in DEFAULT_PHASES.items():
        if keyword in lowered:
            phases.update(mapped)

    if not phases:
        phases.update(registry["autonomous_contract"]["loop"])

    results = []
    for source in registry.get("sources", []):
        patterns = source.get("patterns", [])
        pattern_hits = [
            pattern for pattern in patterns
            if _tokens(pattern) & query or pattern.lower() in lowered
        ]
        phase_hits = [phase for phase in source.get("nexus_mapping", []) if phase in phases]
        score = len(pattern_hits) * 2 + len(phase_hits)
        if score:
            results.append({
                "repository": source["repository"],
                "role": source["role"],
                "patterns": pattern_hits or patterns[:3],
                "lifecycle_phases": phase_hits,
                "readiness": "reference",
                "execution_allowed": False,
                "score": score,
            })

    results.sort(key=lambda item: (-item["score"], item["repository"]))
    return results[:max(1, limit)]
