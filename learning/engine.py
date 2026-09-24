""""Bounded experience-driven learning engine for Gungv-Nexus."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from intelligence.memory_policy import should_promote, should_store
from intelligence.reflection import reflect
from integrations.capability_health import learn_from_outcome
from memory.experience_store import Experience, ExperienceStore


@dataclass
class LearningEngine:
    experiences: ExperienceStore = field(default_factory=ExperienceStore)

    def observe(self, task: str, plan: list[dict], capabilities: list[str],
                success: bool, quality: float, reward: float,
                errors: list[str] | None = None,
                lessons: list[str] | None = None,
                destructive: bool = False) -> dict[str, Any]:
        outcome = {"success": success, "quality": quality, "reward": reward,
                   "errors": errors or []}
        prior = self.experiences.lessons_for(task, limit=5)
        reflection = reflect(task, outcome, prior)
        confidence = float(reflection["confidence"])
        store_allowed = should_store(
            reward=float(reward), quality=float(quality),
            confidence=confidence, destructive=destructive)
        promoted = should_promote(
            reward=float(reward), quality=float(quality),
            confidence=confidence,
            evidence_count=max(1, int(reflection["evidence_count"])))

        lesson_records = []
        if store_allowed:
            lesson_records.append(reflection)
            lesson_records.extend(
                {"lesson": lesson, "type": "strategic", "confidence": confidence,
                 "evidence_count": 1}
                for lesson in (lessons or [])
                if lesson != reflection["lesson"]
            )

        exp = Experience(
            task=task, plan=plan, capabilities_used=capabilities,
            result="success" if success else "failure",
            errors=errors or [], quality=quality, reward=reward,
            lessons=[r["lesson"] for r in lesson_records],
            lesson_records=lesson_records,
        )
        recorded = self.experiences.record(exp)
        return {"experience": recorded, "reflection": reflection,
                "memory_stored": store_allowed, "lesson_promoted": promoted}

    def learn_provider(self, provider: dict, *, success: bool,
                       quality: float, reward: float) -> dict:
        updated = learn_from_outcome(provider, success=success,
                                     quality=quality, reward=reward)
        provider["learning"] = updated
        return provider

    def context(self, task: str, limit: int = 5) -> dict[str, list[dict]]:
        return {"experiences": self.experiences.similar(task, limit),
                "lessons": self.experiences.lessons_for(task, limit)}

    def promote_lesson(self, lesson: str, reward: float,
                       threshold: float = 0.7) -> bool:
        return float(reward) >= float(threshold)
