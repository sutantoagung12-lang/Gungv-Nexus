"""Bounded experience-driven learning engine for Gungv-Nexus."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from integrations.capability_health import learn_from_outcome
from memory.experience_store import Experience, ExperienceStore


@dataclass
class LearningEngine:
    experiences: ExperienceStore = field(default_factory=ExperienceStore)

    def observe(self, task: str, plan: list[dict], capabilities: list[str],
                success: bool, quality: float, reward: float,
                errors: list[str] | None = None,
                lessons: list[str] | None = None) -> dict[str, Any]:
        exp = Experience(
            task=task, plan=plan, capabilities_used=capabilities,
            result="success" if success else "failure",
            errors=errors or [], quality=quality, reward=reward,
            lessons=lessons or [],
        )
        return self.experiences.record(exp)

    def learn_provider(self, provider: dict, *, success: bool,
                       quality: float, reward: float) -> dict:
        updated = learn_from_outcome(provider, success=success,
                                     quality=quality, reward=reward)
        provider["learning"] = updated
        return provider

    def context(self, task: str, limit: int = 5) -> dict[str, list[dict]]:
        return {
            "experiences": self.experiences.similar(task, limit),
            "lessons": self.experiences.lessons_for(task, limit),
        }

    def promote_lesson(self, lesson: str, reward: float,
                       threshold: float = 0.7) -> bool:
        return float(reward) >= float(threshold)
