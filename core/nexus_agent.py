"""Unified Gungv-Nexus agent.

This is the single structural entry point for the whole cognitive system.
Subsystems remain modular internally, but the public architecture is one agent:
input -> cognition -> capability selection -> guarded execution -> verification
-> memory/learning -> evolution -> sleep/wake.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from agents.orchestrator import Orchestrator
from integrations.autonomous_runtime import AutonomousRuntime
from integrations.autonomous_skill_resolver import resolve_autonomous_skills
from integrations.capability_resolver import resolve as resolve_capability
from integrations.runtime import inspect_runtime
from memory.skill_builder import SkillBuilder
from memory.skill_store import SkillStore
from experiments.engine import ExperimentEngine
from skills.ai_dominance import AIDominanceSkill
from skills.domain_expansion import DomainExpansionSkill
from skills.self_evolution import SelfEvolutionSkill


@dataclass
class NexusCycle:
    task: str
    stage: str
    route: dict[str, Any]
    skills: list[dict[str, Any]]
    lifecycle: list[str]
    guards: dict[str, Any]
    next_action: str


class GungvNexusAgent:
    """One agent facade over every Nexus subsystem."""

    LIFECYCLE = (
        "WAKE", "HYDRATE", "UNDERSTAND", "RETRIEVE", "DISCOVER",
        "PLAN", "POLICY_CHECK", "EXECUTE", "CHECKPOINT", "OBSERVE",
        "VERIFY", "LEARN", "EVOLVE", "SLEEP",
    )

    def __init__(self) -> None:
        self.orchestrator = Orchestrator()
        self.runtime = AutonomousRuntime()
        self.skill_store = SkillStore()
        self.skill_builder = SkillBuilder()
        self.experiments = ExperimentEngine()
        self.domain_expansion = DomainExpansionSkill()
        self.self_evolution = SelfEvolutionSkill()
        self.ai_dominance = AIDominanceSkill()

    def think(self, task: str) -> NexusCycle:
        if not isinstance(task, str) or not task.strip():
            raise ValueError("task must be a non-empty string")

        route = self.runtime.plan(task)
        skills = resolve_autonomous_skills(task)
        lifecycle = list(self.LIFECYCLE)

        return NexusCycle(
            task=task,
            stage="PLAN",
            route=route,
            skills=skills,
            lifecycle=lifecycle,
            guards={
                "external_code": "reference_only_until_validated",
                "destructive_actions": "human_approval",
                "promotion": "evidence_and_validation",
                "checkpoint": "required_before_mutation",
                "rollback": "last_verified_checkpoint",
                "failure": "fail_closed",
            },
            next_action="POLICY_CHECK",
        )

    def capabilities(self, task: str) -> dict[str, Any]:
        return resolve_capability(task)

    def health(self) -> dict[str, Any]:
        runtime = inspect_runtime()
        return {
            "agent": "GungvNexusAgent",
            "architecture": "single-agent-unified",
            "runtime": runtime,
            "lifecycle": list(self.LIFECYCLE),
            "subsystems": [
                "orchestrator", "autonomous-runtime", "capability-resolver",
                "memory", "knowledge", "skills", "experiments",
                "domain-expansion", "self-evolution", "ai-dominance",
            ],
        }

    def contract(self) -> dict[str, Any]:
        return {
            "identity": "Gungv-Nexus",
            "agent": "GungvNexusAgent",
            "architecture": "one-agent-composed-system",
            "control_loop": list(self.LIFECYCLE),
            "principle": "one decision surface, modular internal organs",
            "execution": "guarded-and-validated",
            "learning": "memory-and-evidence",
            "evolution": "experiment-and-rollback",
        }
