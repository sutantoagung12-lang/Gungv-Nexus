"""Health and learning signals for capability providers."""
from __future__ import annotations

READINESS_SCORE = {"ready": 1.0, "validated": 1.0, "configured": 0.75, "installed": 0.5, "unavailable": 0.0}

def score(provider: dict, *, success_rate: float = 0.5, quality: float = 0.5,
          reward: float | None = None, reliability: float | None = None) -> float:
    success_rate = max(0.0, min(1.0, success_rate))
    quality = max(0.0, min(1.0, quality))
    reward = quality if reward is None else reward
    reliability = success_rate if reliability is None else reliability
    readiness = READINESS_SCORE.get(provider.get("readiness", "unavailable"), 0.0)
    trust = 1.0 if provider.get("trust") in {"external-public", "trusted"} else 0.5
    values = [max(0.0, min(1.0, x)) for x in (success_rate, quality, reward, reliability)]
    return round(0.30 * readiness + 0.10 * trust + 0.22 * values[0] + 0.16 * values[1] + 0.12 * values[2] + 0.10 * values[3], 4)

def rank(providers: list[dict], telemetry: dict | None = None) -> list[dict]:
    telemetry = telemetry or {}
    ranked = []
    for provider in providers:
        stats = telemetry.get(provider["repository"], {})
        item = dict(provider)
        item["health_score"] = score(
            provider,
            success_rate=stats.get("success_rate", 0.5),
            quality=stats.get("quality", 0.5),
            reward=stats.get("reward"),
            reliability=stats.get("reliability"),
        )
        ranked.append(item)
    return sorted(ranked, key=lambda x: (-x["health_score"], x["repository"]))
