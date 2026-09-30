"""Functional consciousness model: awareness, attention and metacognition."""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ConsciousState:
    awareness: str = "INITIAL"
    attention: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    self_awareness: dict[str, Any] = field(default_factory=dict)
    reflections: list[str] = field(default_factory=list)

class Consciousness:
    """Models functional awareness; it does not claim subjective experience."""
    def __init__(self):
        self.state = ConsciousState()

    def perceive(self, context: dict[str, Any]) -> dict[str, Any]:
        self.state.context = dict(context)
        self.state.awareness = "AWARE"
        return self.snapshot()

    def attend(self, subject: str) -> dict[str, Any]:
        self.state.attention = subject
        self.state.awareness = "ATTENDING"
        return self.snapshot()

    def introspect(self, self_model: dict[str, Any]) -> dict[str, Any]:
        self.state.self_awareness = dict(self_model)
        return {"status": "INTROSPECTED", "self_awareness": dict(self_model)}

    def reflect(self, observation: str) -> dict[str, Any]:
        self.state.reflections.append(observation)
        self.state.reflections = self.state.reflections[-100:]
        return {"status": "REFLECTED", "observation": observation}

    def snapshot(self) -> dict[str, Any]:
        return {
            "awareness": self.state.awareness,
            "attention": self.state.attention,
            "context_keys": sorted(self.state.context),
            "self_aware": bool(self.state.self_awareness),
            "reflection_count": len(self.state.reflections),
        }
