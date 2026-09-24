"""Bounded fallback planning. It never executes actions itself."""
from __future__ import annotations


def build_plan(candidates: list[dict], max_attempts: int = 3) -> list[dict]:
    plan = []
    for item in candidates:
        for provider in item.get("providers", [])[:max_attempts]:
            attempt = 1 + sum(p["capability"] == item["capability"] for p in plan)
            plan.append({"capability": item["capability"], "repository": provider["repository"], "health_score": provider.get("health_score", 0.0), "attempt": attempt})
    return plan
