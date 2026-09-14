from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryProfile:
    name: str
    full_name: str
    capabilities: frozenset[str]
    access_mode: str = "read_only"
    integration_mode: str = "adapter"
    enabled: bool = True
    maintenance_score: float = 0.5
    security_score: float = 0.5
    integration_cost: float = 0.5


@dataclass(frozen=True)
class Evaluation:
    full_name: str
    score: float
    matched_capabilities: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    recommendation: str


def evaluate(profile: RepositoryProfile, required: set[str]) -> Evaluation:
    matched = required & set(profile.capabilities)
    missing = required - matched
    capability_score = len(matched) / len(required) if required else 1.0
    safety = 1.0 if profile.access_mode == "read_only" else 0.5
    quality = (profile.maintenance_score + profile.security_score) / 2
    cost = max(0.0, min(1.0, 1.0 - profile.integration_cost))
    score = round(0.55 * capability_score + 0.2 * quality + 0.15 * safety + 0.1 * cost, 4)
    if not profile.enabled:
        recommendation = "disabled"
    elif score >= 0.8 and not missing:
        recommendation = "adopt_candidate"
    elif score >= 0.6:
        recommendation = "evaluate_further"
    else:
        recommendation = "observe"
    return Evaluation(profile.full_name, score, tuple(sorted(matched)), tuple(sorted(missing)), recommendation)


def rank(profiles: list[RepositoryProfile], required: set[str]) -> list[Evaluation]:
    return sorted((evaluate(p, required) for p in profiles), key=lambda item: item.score, reverse=True)
