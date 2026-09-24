"""Health and learning signals for capability providers."""
from __future__ import annotations

READINESS_SCORE = {"ready": 1.0, "validated": 1.0, "configured": 0.75, "installed": 0.5, "unavailable": 0.0}


def score(provider: dict, *, success_rate: float = 0.5, quality: float = 0.5,
          reward: float = 0.5, reliability: float = 0.5) -> float:
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
            reward=stats.get("reward", 0.5),
            reliability=stats.get("reliability", 0.5),
        )
        ranked.append(item)
    return sorted(ranked, key=lambda x: (-x["health_score"], x["repository"]))


def learn_from_outcome(provider: dict, *, success: bool, quality: float,
                       reward: float, alpha: float = 0.2) -> dict:
    """Return updated exponential-moving estimates; caller owns persistence."""
    old = provider.get("learning", {})
    def ema(name: str, value: float) -> float:
        previous = float(old.get(name, 0.5))
        return round((1 - alpha) * previous + alpha * max(0.0, min(1.0, value)), 4)
    return {
        "success_rate": ema("success_rate", 1.0 if success else 0.0),
        "quality": ema("quality", quality),
        "reward": ema("reward", reward),
        "reliability": ema("reliability", 1.0 if success else 0.0),
    }
