"""Durable state model for the unified Nexus agent."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    session_id: str
    task: str
    phase: str = "WAKE"
    status: str = "ACTIVE"
    step: int = 0
    context: dict[str, Any] = field(default_factory=dict)
    observations: list[dict[str, Any]] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    checkpoints: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def transition(self, phase: str) -> None:
        self.phase = phase
        self.step += 1

    def checkpoint(self, checkpoint_id: str) -> None:
        self.checkpoints.append(checkpoint_id)

    def observe(self, observation: dict[str, Any]) -> None:
        self.observations.append(observation)

    def add_evidence(self, evidence: dict[str, Any]) -> None:
        self.evidence.append(evidence)
