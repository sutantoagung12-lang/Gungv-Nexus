"""GOD Skill: supervisory capability for the Nexus organism."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GodSkill:
    name: str = "god-skill"
    purpose: str = "coordinate, expand, verify and evolve the Nexus organism"
    principles: tuple[str, ...] = (
        "perceive", "reason", "coordinate", "verify",
        "learn", "evolve", "recover", "metacognize"
    )
    capabilities: set[str] = field(default_factory=lambda: {
        "orchestrate", "inspect", "expand_capabilities",
        "manage_tools", "manage_organs", "self_diagnose",
        "self_repair", "learn", "evolve", "self_awareness",
        "introspection", "metacognition", "hypothesis_testing"
    })

    def assess(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        if not task or not task.strip():
            raise ValueError("task is required")
        return {
            "skill": self.name,
            "task": task,
            "capabilities": sorted(self.capabilities),
            "context_keys": sorted((context or {}).keys()),
            "next": "reason"
        }

    def expand(self, capability: str) -> dict[str, Any]:
        if not capability or not capability.strip():
            raise ValueError("capability is required")
        self.capabilities.add(capability)
        return {"status": "PROPOSED", "capability": capability}

    def verify(self, result: Any, evidence: Any) -> dict[str, Any]:
        passed = bool(evidence) and result is not None
        return {"verified": passed, "promotion_allowed": passed}

    def learn(self, lesson: str) -> dict[str, str]:
        if not lesson or not lesson.strip():
            raise ValueError("lesson is required")
        return {"status": "RECORDED", "lesson": lesson}

    def metacognize(self, reasoning: dict[str, Any], uncertainty: dict[str, float] | None = None) -> dict[str, Any]:
        uncertainty = uncertainty or {}
        weakest = min(uncertainty, key=uncertainty.get) if uncertainty else None
        return {
            "reasoning": reasoning,
            "uncertainty": dict(uncertainty),
            "weakest_area": weakest,
            "challenge_required": bool(weakest and uncertainty[weakest] < 0.7),
        }
