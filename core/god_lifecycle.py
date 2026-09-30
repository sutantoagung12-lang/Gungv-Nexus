"""GOD-CORE lifecycle coordinator with explicit metacognitive verification."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GodLifecycle:
    god: Any
    phase: str = "DORMANT"
    history: list[str] = field(default_factory=list)

    PHASES = (
        "WAKE", "PERCEIVE", "UNDERSTAND", "REASON", "CHALLENGE",
        "DECIDE", "ACT", "CHECKPOINT", "OBSERVE", "VERIFY",
        "LEARN", "EVOLVE", "SLEEP",
    )

    def step(self, phase: str) -> str:
        if phase not in self.PHASES:
            raise ValueError(f"unknown phase: {phase}")
        self.phase = phase
        self.history.append(phase)
        return phase

    def run(self, task: str) -> dict[str, Any]:
        if not task or not task.strip():
            raise ValueError("task is required")
        self.history = []

        self.step("WAKE")
        self.god.awaken(task)

        self.step("PERCEIVE")
        perception = self.god.perceive(task)

        self.step("UNDERSTAND")
        reasoning = self.god.reason(task)

        self.step("REASON")
        self.step("CHALLENGE")
        metacognition = self.god.metacognize(
            task,
            reasoning,
            {"task_interpretation": 0.8, "capability_fit": 0.8},
        )

        self.step("DECIDE")
        decision = {
            "status": "READY",
            "challenge_required": metacognition["challenge_required"],
            "weakest_area": metacognition["weakest_area"],
        }

        self.step("ACT")
        self.step("CHECKPOINT")
        self.step("OBSERVE")
        observation = {
            "task": task,
            "perception": perception,
            "reasoning": reasoning,
            "metacognition": metacognition,
            "decision": decision,
        }

        self.step("VERIFY")
        verified = bool(reasoning) and bool(perception)
        self.god.record_evidence({
            "task": task,
            "verified": verified,
            "metacognition": metacognition,
        })

        self.step("LEARN")
        self.god.reflect({
            "task": task,
            "verified": verified,
            "weakest_area": metacognition["weakest_area"],
        })

        self.step("EVOLVE")
        self.step("SLEEP")
        self.god.sleep()

        return {
            "status": "COMPLETED" if verified else "VERIFICATION_FAILED",
            "task": task,
            "verified": verified,
            "phases": list(self.history),
            "observation": observation,
        }
