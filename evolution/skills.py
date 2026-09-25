"""Quality-gated skill extraction from repeated experience."""
from __future__ import annotations

from memory.skill_store import Skill, SkillStore


class SkillLearning:
    MIN_EVIDENCE = 2
    MIN_QUALITY = 0.8
    MIN_REWARD = 0.8
    MIN_CONFIDENCE = 0.8

    def __init__(self, store: SkillStore):
        self.store = store

    def observe(self, experience: dict) -> dict | None:
        records = experience.get("lesson_records", [])
        if not records:
            return None
        if float(experience.get("quality", 0.0)) < self.MIN_QUALITY:
            return None
        if float(experience.get("reward", 0.0)) < self.MIN_REWARD:
            return None

        lesson = records[0].get("lesson", "").strip()
        if not lesson:
            return None
        confidence = float(records[0].get("confidence", 0.0))
        if confidence < self.MIN_CONFIDENCE:
            return None

        skill_id = self.store.stable_id(lesson)
        prior = next((s for s in self.store.all() if s.get("skill_id") == skill_id), None)
        evidence = int(prior.get("evidence_count", 0)) if prior else 0
        evidence += 1
        task = experience.get("task", "").strip()
        skill = Skill(
            skill_id=skill_id,
            name=f"learned-{skill_id}",
            description=f"Reusable procedure for tasks matching: {task}",
            procedure=lesson,
            source_lessons=[lesson],
            evidence_count=evidence,
            quality=float(experience.get("quality", 0.0)),
            reward=float(experience.get("reward", 0.0)),
            confidence=confidence,
            status="ACTIVE" if evidence >= self.MIN_EVIDENCE else "PROPOSED",
        )
        return self.store.upsert(skill)

    def retrieve(self, task: str, limit: int = 5) -> list[dict]:
        return self.store.search(task, limit)
