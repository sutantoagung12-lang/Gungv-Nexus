from __future__ import annotations

from dataclasses import dataclass, field
from math import log1p
from typing import Any


@dataclass(frozen=True)
class TaskProfile:
    """Normalized task requirements used by the adaptive router."""

    kind: str
    complexity: float = 0.5
    risk: float = 0.1
    reasoning: float = 0.0
    coding: float = 0.0
    research: float = 0.0
    multimodal: float = 0.0
    tool_use: float = 0.0
    latency_budget: float = 1.0
    cost_budget: float = 1.0

    def __post_init__(self) -> None:
        for name in (
            "complexity", "risk", "reasoning", "coding", "research",
            "multimodal", "tool_use", "latency_budget", "cost_budget",
        ):
            value = float(getattr(self, name))
            if value < 0:
                raise ValueError(f"{name} must be non-negative")


@dataclass
class ModelProfile:
    """Provider-neutral model capability and observed-performance profile."""

    name: str
    capabilities: dict[str, float] = field(default_factory=dict)
    latency: float = 1.0
    cost: float = 1.0
    reliability: float = 0.8
    privacy: float = 0.5
    successes: int = 0
    failures: int = 0

    @property
    def observed_reliability(self) -> float:
        total = self.successes + self.failures
        if total == 0:
            return max(0.0, min(1.0, self.reliability))
        # Shrink small samples toward the declared prior.
        prior_weight = 5
        return (self.reliability * prior_weight + self.successes) / (prior_weight + total)

    def capability(self, name: str) -> float:
        return max(0.0, min(1.0, float(self.capabilities.get(name, 0.0))))

    def record(self, success: bool) -> None:
        if success:
            self.successes += 1
        else:
            self.failures += 1


class AdaptiveRouter:
    """Low-overhead capability router with experience-based adaptation.

    The router intentionally uses a transparent score rather than embedding
    provider-specific assumptions. New models can be registered without
    changing orchestration code.
    """

    _weights = {
        "reasoning": 1.6,
        "coding": 1.5,
        "research": 1.3,
        "multimodal": 1.4,
        "tool_use": 1.5,
    }

    def __init__(self, models: list[ModelProfile] | None = None) -> None:
        self.models: dict[str, ModelProfile] = {m.name: m for m in models or []}

    def register(self, model: ModelProfile) -> ModelProfile:
        self.models[model.name] = model
        return model

    def score(self, task: TaskProfile, model: ModelProfile) -> float:
        requirements = {
            "reasoning": task.reasoning,
            "coding": task.coding,
            "research": task.research,
            "multimodal": task.multimodal,
            "tool_use": task.tool_use,
        }
        capability_fit = 0.0
        capability_weight = 0.0
        for key, requirement in requirements.items():
            if requirement <= 0:
                continue
            weight = self._weights[key] * requirement
            capability_fit += model.capability(key) * weight
            capability_weight += weight
        if capability_weight:
            capability_fit /= capability_weight

        latency_penalty = min(1.0, model.latency / max(task.latency_budget, 0.01))
        cost_penalty = min(1.0, model.cost / max(task.cost_budget, 0.01))
        risk_fit = model.observed_reliability * (0.6 + 0.4 * model.privacy)
        experience_bonus = min(0.15, log1p(model.successes) / 100)

        # Higher complexity/risk makes reliability matter more; cheap/fast
        # models still win routine work because penalties are explicit.
        reliability_weight = 0.9 + 1.4 * task.complexity + 1.8 * task.risk
        return (
            capability_fit * 4.0
            + risk_fit * reliability_weight
            + experience_bonus
            - latency_penalty * (0.5 + 0.5 * (1.0 - task.complexity))
            - cost_penalty * 0.45
        )

    def rank(self, task: TaskProfile, limit: int = 3) -> list[tuple[ModelProfile, float]]:
        if limit < 1:
            return []
        ranked = ((model, self.score(task, model)) for model in self.models.values())
        return sorted(ranked, key=lambda item: item[1], reverse=True)[:limit]

    def choose(self, task: TaskProfile) -> ModelProfile | None:
        ranked = self.rank(task, limit=1)
        return ranked[0][0] if ranked else None

    def learn(self, model_name: str, success: bool) -> None:
        model = self.models.get(model_name)
        if model is not None:
            model.record(success)


def plan_parallelism(task: TaskProfile) -> int:
    """Choose a bounded swarm width from complexity and risk."""
    signal = max(task.complexity, task.research, task.reasoning)
    if signal < 0.35:
        return 1
    if signal < 0.65:
        return 3
    if signal < 0.85:
        return 6
    return 10 if task.risk < 0.8 else 4
