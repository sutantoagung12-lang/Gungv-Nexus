"""Evidence-informed intelligence architecture for Gungv-Nexus.

Combines planning, tools, memory, evaluation, experience learning, selective
foresight, and safety gates without making autonomous external changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntelligenceProfile:
    memory: bool = True
    planning: bool = True
    tool_selection: bool = True
    evaluation: bool = True
    experience_learning: bool = True
    foresight: bool = True
    uncertainty_gating: bool = True
    safety_gating: bool = True
    reflection: bool = True
    quality_aware_memory: bool = True
    multi_agent: bool = True


@dataclass
class IntelligenceCycle:
    task: str
    context: dict[str, Any] = field(default_factory=dict)
    plan: list[dict[str, Any]] = field(default_factory=list)
    candidate_actions: list[dict[str, Any]] = field(default_factory=list)
    selected_action: dict[str, Any] | None = None
    confidence: float = 0.0
    requires_review: bool = False

    def add_plan_step(self, step: dict[str, Any]) -> None:
        self.plan.append(step)

    def select_action(self, actions: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not actions:
            self.selected_action = None
            return None
        ranked = sorted(
            actions,
            key=lambda x: (
                -float(x.get("expected_value", 0.0)),
                float(x.get("risk", 1.0)),
                float(x.get("cost", 1.0)),
            ),
        )
        self.candidate_actions = ranked
        self.selected_action = ranked[0]
        self.confidence = max(0.0, min(1.0, float(ranked[0].get("confidence", 0.0))))
        self.requires_review = (
            bool(ranked[0].get("destructive", False))
            or self.confidence < 0.55
            or float(ranked[0].get("risk", 0.0)) >= 0.7
        )
        return self.selected_action


DEFAULT_PROFILE = IntelligenceProfile()
