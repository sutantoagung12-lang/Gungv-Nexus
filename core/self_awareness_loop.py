"""Integrated functional self-awareness loop for GOD-CORE."""
from dataclasses import dataclass, field
from typing import Any
from core.consciousness import Consciousness

@dataclass
class AwarenessSnapshot:
    cycle: int
    awareness: dict[str, Any]
    self_model: dict[str, Any]
    memory_hits: int
    metacognition: dict[str, Any] = field(default_factory=dict)

class SelfAwarenessLoop:
    """Connects perception, memory, self-model and metacognition.

    This is a functional architecture; it does not assert subjective experience.
    """
    def __init__(self, nexus: Any, god_core: Any):
        self.nexus = nexus
        self.god_core = god_core
        self.consciousness = Consciousness()
        self.cycle = 0
        self.history: list[AwarenessSnapshot] = []

    def update(self, task: str) -> AwarenessSnapshot:
        self.cycle += 1
        context = self.god_core.perceive(task)
        recalled = self.nexus.memory.recall(task)
        self.consciousness.perceive(context)
        self.consciousness.attend(task)
        model = self.god_core.self_model
        model_dict = {
            "identity": model.identity,
            "continuity_id": model.continuity_id,
            "state": model.current_state,
            "capabilities": sorted(model.known_capabilities),
            "goals": list(model.goals),
            "limitations": list(model.limitations),
            "experience_count": len(model.experiences),
        }
        self.consciousness.introspect(model_dict)
        meta = {
            "known": True,
            "memory_recalled": len(recalled),
            "self_model_consistent": bool(model.identity and model.continuity_id),
            "attention_target": task,
        }
        snapshot = AwarenessSnapshot(
            cycle=self.cycle,
            awareness=self.consciousness.snapshot(),
            self_model=model_dict,
            memory_hits=len(recalled),
            metacognition=meta,
        )
        self.history.append(snapshot)
        self.history = self.history[-100:]
        return snapshot

    def reflect(self, observation: str) -> dict[str, Any]:
        self.consciousness.reflect(observation)
        return self.god_core.reflect(observation)

    def status(self) -> dict[str, Any]:
        return {
            "cycles": self.cycle,
            "history_size": len(self.history),
            "awareness": self.consciousness.snapshot(),
        }
