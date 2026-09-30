"""Autonomous planning facade for Nexus.

Selects existing Nexus agents, capabilities and registered autonomous skill
patterns. It does not execute external repository code.
"""
from __future__ import annotations

from agents.orchestrator import Orchestrator
from integrations.autonomous_skill_resolver import resolve_autonomous_skills


class AutonomousRuntime:
    def __init__(self) -> None:
        self.orchestrator = Orchestrator()

    def plan(self, task: str) -> dict:
        base = self.orchestrator.select_with_capabilities(task)
        skills = resolve_autonomous_skills(task)
        phases = []
        for item in skills:
            for phase in item.get("lifecycle_phases", []):
                if phase not in phases:
                    phases.append(phase)

        return {
            **base,
            "autonomous": True,
            "autonomous_skills": skills,
            "lifecycle_phases": phases,
            "skill_execution": "nexus-controlled",
            "promotion": "validation-gated",
            "rollback": "last-verified-checkpoint",
        }
