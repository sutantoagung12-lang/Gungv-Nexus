from pathlib import Path

import pytest

from memory.skill_builder import SkillBuilder
from memory.skill_store import SkillStore


def test_builder_creates_candidate(tmp_path: Path):
    store = SkillStore(str(tmp_path / "skills.jsonl"))
    candidate = SkillBuilder(store).build(
        "Research Skill",
        "Research and validate AI sources",
        "discover; retrieve; verify",
        ["successful source verification"],
        ["source is cited"],
    )
    assert candidate.skill.status == "CANDIDATE"
    saved = SkillBuilder(store).save_candidate(candidate)
    assert saved["status"] == "CANDIDATE"


def test_builder_requires_validation_for_promotion(tmp_path: Path):
    store = SkillStore(str(tmp_path / "skills.jsonl"))
    builder = SkillBuilder(store)
    candidate = builder.build("Test Skill", "test", "do test", ["lesson"])

    with pytest.raises(ValueError):
        builder.promote(candidate, evidence_count=1, quality=0.7, confidence=0.9)

    active = builder.promote(candidate, evidence_count=2, quality=0.9, confidence=0.9)
    assert active["status"] == "ACTIVE"
