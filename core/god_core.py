"""GOD-CORE supervisory reasoning with self-model and metacognition."""
from dataclasses import dataclass, field
from typing import Any
from skills.god_skill import GodSkill


@dataclass
class SelfModel:
    identity: str = "Gungv-Nexus"
    continuity_id: str = "gungv-nexus"
    current_state: str = "AWAKE"
    self_description: str = "A persistent software organism coordinated by Nexus."
    perceived_context: dict[str, Any] = field(default_factory=dict)
    known_capabilities: set[str] = field(default_factory=set)
    goals: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    experiences: list[dict[str, Any]] = field(default_factory=list)
    self_reflections: list[str] = field(default_factory=list)
    uncertainty: dict[str, float] = field(default_factory=dict)
    hypotheses: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class GodState:
    mode: str = "AWAKE"
    objectives: list[str] = field(default_factory=list)
    capabilities: set[str] = field(default_factory=set)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    cycle: int = 0


class GodCore:
    """Supervisory intelligence with explicit functional metacognition."""

    def __init__(self, nexus: Any):
        self.nexus = nexus
        self.state = GodState()
        self.self_model = SelfModel()
        self.skill = GodSkill()

    def awaken(self, objective: str | None = None) -> GodState:
        self.state.mode = "AWAKE"
        self.self_model.current_state = "AWAKE"
        self.state.cycle += 1
        if objective and objective not in self.state.objectives:
            self.state.objectives.append(objective)
        if objective and objective not in self.self_model.goals:
            self.self_model.goals.append(objective)
        return self.state

    def perceive(self, task: str) -> dict[str, Any]:
        context = {
            "task": task,
            "capabilities": self.nexus.capabilities(),
            "health": self.nexus.health(),
            "contract": self.nexus.contract(),
        }
        self.self_model.perceived_context = context
        self.self_model.known_capabilities = set(context["capabilities"].keys())
        return context

    def reason(self, task: str) -> dict[str, Any]:
        result = self.nexus.think(task).__dict__
        self.self_model.experiences.append({"task": task, "stage": result.get("stage")})
        self.self_model.experiences = self.self_model.experiences[-200:]
        return result

    def generate_hypotheses(self, task: str, alternatives: list[str]) -> list[dict[str, Any]]:
        self.self_model.hypotheses = [
            {"task": task, "option": option, "status": "UNVERIFIED"}
            for option in alternatives
        ]
        return list(self.self_model.hypotheses)

    def evaluate_hypothesis(self, index: int, evidence: Any, supports: bool) -> dict[str, Any]:
        if index < 0 or index >= len(self.self_model.hypotheses):
            return {"status": "INVALID_HYPOTHESIS"}
        item = self.self_model.hypotheses[index]
        item["status"] = "SUPPORTED" if supports else "REJECTED"
        item["evidence"] = evidence
        return item

    def metacognize(self, task: str, reasoning: dict[str, Any], uncertainty: dict[str, float] | None = None) -> dict[str, Any]:
        uncertainty = uncertainty or {}
        self.self_model.uncertainty = dict(uncertainty)
        weakest = min(uncertainty, key=uncertainty.get) if uncertainty else None
        return {
            "task": task,
            "reasoning_stage": reasoning.get("stage"),
            "known_capabilities": len(self.self_model.known_capabilities),
            "memory_available": bool(self.self_model.perceived_context),
            "uncertainty": dict(uncertainty),
            "weakest_area": weakest,
            "challenge_required": bool(weakest and uncertainty[weakest] < 0.7),
        }

    def assess_self(self, task: str = "self assessment") -> dict[str, Any]:
        return self.skill.assess(task, {
            "identity": self.self_model.identity,
            "state": self.self_model.current_state,
            "capabilities": sorted(self.self_model.known_capabilities),
            "goals": list(self.self_model.goals),
            "limitations": list(self.self_model.limitations),
            "cycle": self.state.cycle,
            "uncertainty": dict(self.self_model.uncertainty),
        })

    def reflect(self, observation: str) -> dict[str, Any]:
        self.self_model.self_reflections.append(observation)
        self.self_model.self_reflections = self.self_model.self_reflections[-100:]
        return {"status": "REFLECTED", "identity": self.self_model.identity, "observation": observation}

    def propose_evolution(self, capability: str, reason: str) -> dict[str, Any]:
        return self.nexus.propose_capability(capability, reason)

    def propose_organ(self, organ_id: str, name: str, function: str) -> dict[str, Any]:
        return self.nexus.propose_organ(organ_id, name, function)

    def record_evidence(self, evidence: dict[str, Any]) -> None:
        self.state.evidence.append(evidence)

    def sleep(self) -> GodState:
        self.state.mode = "SLEEP"
        self.self_model.current_state = "SLEEP"
        return self.state
