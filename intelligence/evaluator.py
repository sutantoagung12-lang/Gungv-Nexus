"""Bounded evaluator for outcome quality, risk, and learning reward."""
from __future__ import annotations


def evaluate(*, success: bool, quality: float, risk: float = 0.0,
             cost: float = 0.0, efficiency: float = 1.0) -> dict[str, float | bool]:
    q = max(0.0, min(1.0, quality))
    r = max(0.0, min(1.0, risk))
    e = max(0.0, min(1.0, efficiency))
    reward = (0.50 * (1.0 if success else 0.0) +
              0.30 * q +
              0.15 * e -
              0.15 * r -
              0.05 * max(0.0, cost))
    reward = round(max(0.0, min(1.0, reward)), 4)
    return {"success": bool(success), "quality": round(q, 4),
            "risk": round(r, 4), "efficiency": round(e, 4),
            "reward": reward}
