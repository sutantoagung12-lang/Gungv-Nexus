"""Unified Nexus agent controller.

Single-agent control plane that composes routing, autonomous skills, lifecycle,
memory/knowledge intent, experimentation and guarded evolution. Planning is
deterministic and fail-closed; external reference code is never executed here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from integrations.autonomous_runtime import AutonomousRuntime
from integrations.runtime_availability import RuntimeAvailability
from skills.domain_expansion import DomainExpansionSkill
from skills.self_evolution import SelfEvolutionSkill


@dataclass
class AgentDecision:
    task: str
    phase: str
    plan: list[str]
    capabilities: dict[str, Any]
    skills: list[dict[str, Any]]
    experiments: list[dict[str, Any]] = field(default_factory=list)
    guardrails: dict[str, Any] = field(default_factory=dict)
    status: str = "PLANNED"


class NexusAgent:
    """One logical agent over all Nexus subsystems."""

    LIFECYCLE = (
        "WAKE", "HYDRATE", "UNDERSTAND", "RETRIEVE", "DISCOVER",
        "PLAN", "POLICY_CHECK", "EXECUTE", "CHECKPOINT", "OBSERVE",
        "VERIFY", "LEARN", "EVOLVE", "SLEEP",
    )

    def __init__(self) -> None:
        self.runtime = AutonomousRuntime()
        self.availability = RuntimeAvailability()
        self.domain = DomainExpansionSkill()
        self.evolution = SelfEvolutionSkill()

    def plan(self, task: str) -> AgentDecision:
        if not isinstance(task, str) or not task.strip():
            raise ValueError("task must be a non-empty string")

        route = self.runtime.plan(task)
        capabilities = route.get("capabilities", {})
        skills = route.get("autonomous_skills", [])
        phases = route.get("lifecycle_phases", [])

        plan = [
            "WAKE", "HYDRATE", "UNDERSTAND", "RETRIEVE", "DISCOVER",
            "PLAN", "POLICY_CHECK", "EXECUTE", "CHECKPOINT",
            "OBSERVE", "VERIFY", "LEARN",
        ]
        if any(p in phases for p in ("EVOLVE", "LEARN", "RECOVER")):
            plan.append("EVOLVE")
        plan.append("SLEEP")

        return AgentDecision(
            task=task,
            phase="PLAN",
            plan=list(dict.fromkeys(plan)),
            capabilities=capabilities,
            skills=skills,
            guardrails={
                "external_reference_execution": False,
                "destructive_actions": "approval_required",
                "promotion": "validation_gated",
                "checkpoint": "before_mutation",
                "rollback": "last_verified_checkpoint",
                "fail_closed": True,
            },
        )

    def status(self) -> dict[str, Any]:
        return {
            "agent": "NexusAgent",
            "mode": "unified-single-agent",
            "lifecycle": list(self.LIFECYCLE),
            "execution_policy": "Nexus-controlled",
            "promotion_policy": "validation-gated",
            "rollback_policy": "last-verified-checkpoint",
        }
