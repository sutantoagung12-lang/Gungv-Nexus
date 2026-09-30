"""Quality-gated skill builder for Nexus.

Creates candidate skills from observed lessons. Candidates are never activated
automatically; promotion requires explicit validation evidence.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from memory.skill_store import Skill, SkillStore


@dataclass
class SkillCandidate:
    skill: Skill
    acceptance_criteria: list[str]
    source_lessons: list[str]


class SkillBuilder:
    """Distill reusable procedures from lessons into validation-gated skills."""

    def __init__(self, store: SkillStore):
        self.store = store

    @staticmethod
    def _slug(text: str) -> str:
        words = re.findall(r"[a-z0-9]+", text.lower())
        return "-".join(words[:8]) or "generated-skill"

    def build(
        self,
        name: str,
        description: str,
        procedure: str,
        lessons: Iterable[str],
        acceptance_criteria: Iterable[str] | None = None,
    ) -> SkillCandidate:
        lesson_list = [x.strip() for x in lessons if x and x.strip()]
        criteria = [x.strip() for x in (acceptance_criteria or []) if x and x.strip()]
        lesson_key = " | ".join(lesson_list) or procedure
        skill_id = "candidate-" + SkillStore.stable_id(lesson_key)
        skill = Skill(
            skill_id=skill_id,
            name=name.strip(),
            description=description.strip(),
            procedure=procedure.strip(),
            source_lessons=lesson_list,
            evidence_count=0,
            quality=0.0,
            reward=0.0,
            confidence=0.0,
            status="CANDIDATE",
        )
        return SkillCandidate(skill=skill, acceptance_criteria=criteria,
                              source_lessons=lesson_list)

    def promote(self, candidate: SkillCandidate, evidence_count: int,
                quality: float, confidence: float) -> dict:
        if evidence_count < 1:
            raise ValueError("promotion requires evidence")
        if not 0.0 <= quality <= 1.0 or not 0.0 <= confidence <= 1.0:
            raise ValueError("quality and confidence must be between 0 and 1")
        if quality < 0.8 or confidence < 0.8:
            raise ValueError("promotion gate requires quality and confidence >= 0.8")

        candidate.skill.evidence_count = evidence_count
        candidate.skill.quality = quality
        candidate.skill.confidence = confidence
        candidate.skill.status = "ACTIVE"
        return self.store.upsert(candidate.skill)

    def save_candidate(self, candidate: SkillCandidate) -> dict:
        return self.store.upsert(candidate.skill)
