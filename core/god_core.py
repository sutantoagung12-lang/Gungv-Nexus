"""GOD-CORE: top-level coordination layer for Gungv-Nexus.
It coordinates knowledge, reasoning, memory, agents, skills, tools and evolution.
It does not bypass authorization, validation or rollback controls.
"""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class GodState:
    mode: str = 'AWAKE'
    objectives: list[str] = field(default_factory=list)
    capabilities: set[str] = field(default_factory=set)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    cycle: int = 0

class GodCore:
    """A supervisory intelligence layer above the Nexus organism."""
    def __init__(self, nexus: Any):
        self.nexus = nexus
        self.state = GodState()

    def awaken(self, objective: str | None = None) -> GodState:
        self.state.mode = 'AWAKE'
        self.state.cycle += 1
        if objective and objective not in self.state.objectives:
            self.state.objectives.append(objective)
        return self.state

    def perceive(self, task: str) -> dict[str, Any]:
        return {
            'task': task,
            'capabilities': self.nexus.capabilities(),
            'health': self.nexus.health(),
            'contract': self.nexus.contract(),
        }

    def reason(self, task: str) -> dict[str, Any]:
        return self.nexus.think(task).__dict__

    def propose_evolution(self, capability: str, reason: str) -> dict[str, Any]:
        return self.nexus.propose_capability(capability, reason)

    def propose_organ(self, organ_id: str, name: str, function: str) -> dict[str, Any]:
        return self.nexus.propose_organ(organ_id, name, function)

    def record_evidence(self, evidence: dict[str, Any]) -> None:
        self.state.evidence.append(evidence)

    def sleep(self) -> GodState:
        self.state.mode = 'SLEEP'
        return self.state
