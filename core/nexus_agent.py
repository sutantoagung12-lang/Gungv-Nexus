"""Unified Gungv-Nexus agent.

This is the single structural entry point for the whole cognitive system.
Subsystems remain modular internally, but the public architecture is one agent:
input -> cognition -> capability selection -> guarded execution -> verification
-> memory/learning -> evolution -> sleep/wake.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
from core.agent_state import AgentState
from core.agent_memory import AgentMemory
from core.agent_policy import AgentPolicy
from core.agent_event_bus import AgentEventBus
from core.agent_planner import AgentPlanner
from core.agent_goal import GoalManager
from core.agent_reasoning import ReasoningEngine
from core.agent_recovery import RecoveryEngine
from core.agent_evaluator import AgentEvaluator
from core.agent_checkpoint import CheckpointManager
from core.agent_scheduler import AgentScheduler

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
        self.memory = AgentMemory()
        self.policy = AgentPolicy()
        self.events = AgentEventBus()
        self.planner = AgentPlanner()
        self.goals = GoalManager()
        self.reasoning = ReasoningEngine()
        self.recovery = RecoveryEngine()
        self.evaluator = AgentEvaluator()
        self.checkpoints = CheckpointManager()
        self.scheduler = AgentScheduler()

    def think(self, task: str) -> NexusCycle:
        if not isinstance(task, str) or not task.strip():
            raise ValueError("task must be a non-empty string")

        route = self.runtime.plan(task)
        skills = resolve_autonomous_skills(task)
        recalled = self.memory.recall(task)
        reasoning = self.reasoning.analyze(task, {'memory': len(recalled), 'route': route})
        plan = self.planner.build(task, route.get('capabilities', {}), recalled)
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
                "memory_hits": len(recalled),
                "planner": plan,\n                "reasoning": reasoning,
            },
            next_action="POLICY_CHECK",
        )

    def schedule(self, task: str, priority: int = 50) -> int:\n        return self.scheduler.submit(task, priority)\n\n    def recover(self, error: str, attempts: int = 0) -> dict[str, Any]:\n        return self.recovery.diagnose(error, attempts)\n\n    def evaluate(self, expected: Any, observed: Any, evidence: dict[str, Any] | None = None) -> dict[str, Any]:\n        return self.evaluator.evaluate(expected, observed, evidence)\n\n    def checkpoint(self, state_id: str, state: dict[str, Any]) -> dict[str, Any]:\n        return self.checkpoints.create(state_id, state)\n\n    def authorize(self, action: str, *, human_approved=False, environment_validated=False) -> dict[str, Any]:
        return self.policy.check(action, human_approved=human_approved, environment_validated=environment_validated)

    def new_state(self, session_id: str, task: str) -> AgentState:
        return AgentState(session_id=session_id, task=task)

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
            "memory": "episode-and-skill-coordination",
            "policy": "centralized-authorization-gate",
            "events": "lifecycle-event-bus",
            "state": "durable-session-model",
            "planning": "structured-plan-with-memory-context",\n            "goals": "priority-goal-management",\n            "reasoning": "explicit-structured-reasoning",\n            "recovery": "bounded-recovery-and-rollback",\n            "evaluation": "evidence-based-outcome-checking",\n            "checkpoints": "reversible-state-coordination",\n            "scheduler": "priority-work-queue",
        }
