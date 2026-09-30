"""GOD-CORE supervisory layer with a persistent self-model."""
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

@dataclass
class GodState:
    mode: str = 'AWAKE'
    objectives: list[str] = field(default_factory=list)
    capabilities: set[str] = field(default_factory=set)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    cycle: int = 0

class GodCore:
    """Supervisory intelligence plus an explicit, non-sentient self-model."""
    def __init__(self, nexus: Any):
        self.nexus = nexus
        self.state = GodState()
        self.self_model = SelfModel()
        self.skill = GodSkill()

    def awaken(self, objective: str | None = None) -> GodState:
        self.state.mode = 'AWAKE'
        self.self_model.current_state = 'AWAKE'
        self.state.cycle += 1
        if objective and objective not in self.state.objectives:
            self.state.objectives.append(objective)
        if objective and objective not in self.self_model.goals:
            self.self_model.goals.append(objective)
        return self.state

    def perceive(self, task: str) -> dict[str, Any]:
        context = {
            'task': task,
            'capabilities': self.nexus.capabilities(),
            'health': self.nexus.health(),
            'contract': self.nexus.contract(),
        }
        self.self_model.perceived_context = context
        self.self_model.known_capabilities = set(context['capabilities'].keys())
        return context

    def reason(self, task: str) -> dict[str, Any]:
        result = self.nexus.think(task).__dict__
        self.self_model.experiences.append({'task': task, 'stage': result.get('stage')})
        return result

    def assess_self(self, task: str = "self assessment") -> dict[str, Any]:
        return self.skill.assess(task, {
            'identity': self.self_model.identity,
            'state': self.self_model.current_state,
            'capabilities': sorted(self.self_model.known_capabilities),
            'goals': list(self.self_model.goals),
            'limitations': list(self.self_model.limitations),
            'cycle': self.state.cycle,
        })

    def reflect(self, observation: str) -> dict[str, Any]:
        self.self_model.self_reflections.append(observation)
        self.self_model.self_reflections = self.self_model.self_reflections[-100:]
        return {'status': 'REFLECTED', 'identity': self.self_model.identity, 'observation': observation}

    def propose_evolution(self, capability: str, reason: str) -> dict[str, Any]:
        return self.nexus.propose_capability(capability, reason)

    def propose_organ(self, organ_id: str, name: str, function: str) -> dict[str, Any]:
        return self.nexus.propose_organ(organ_id, name, function)

    def record_evidence(self, evidence: dict[str, Any]) -> None:
        self.state.evidence.append(evidence)

    def sleep(self) -> GodState:
        self.state.mode = 'SLEEP'
        self.self_model.current_state = 'SLEEP'
        return self.state
