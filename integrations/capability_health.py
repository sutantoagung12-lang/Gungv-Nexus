"""Deterministic health scoring for capability providers."""
from __future__ import annotations

READINESS_SCORE = {"ready": 1.0, "validated": 1.0, "configured": 0.75, "installed": 0.5, "unavailable": 0.0}


def score(provider: dict, *, success_rate: float = 0.5, quality: float = 0.5) -> float:
    readiness = READINESS_SCORE.get(provider.get("readiness", "unavailable"), 0.0)
    trust = 1.0 if provider.get("trust") in {"external-public", "trusted"} else 0.5
    success = max(0.0, min(1.0, success_rate))
    quality = max(0.0, min(1.0, quality))
    return round(0.45 * readiness + 0.15 * trust + 0.25 * success + 0.15 * quality, 4)


def rank(providers: list[dict], telemetry: dict | None = None) -> list[dict]:
    telemetry = telemetry or {}
    ranked = []
    for provider in providers:
        stats = telemetry.get(provider["repository"], {})
        item = dict(provider)
        item["health_score"] = score(provider, success_rate=stats.get("success_rate", 0.5), quality=stats.get("quality", 0.5))
        ranked.append(item)
    return sorted(ranked, key=lambda x: (-x["health_score"], x["repository"]))
