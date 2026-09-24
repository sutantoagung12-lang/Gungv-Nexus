import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evolution.skills import SkillLearning
from memory.skill_store import SkillStore


def test_skill_promotes_after_repeated_quality_evidence():
    with tempfile.TemporaryDirectory() as tmp:
        store = SkillStore(str(Path(tmp) / "skills.jsonl"))
        learner = SkillLearning(store)
        experience = {
            "task": "improve agent planning",
            "quality": 0.95,
            "reward": 0.9,
            "lesson_records": [{
                "lesson": "Retrieve prior planning cases before execution",
                "confidence": 0.9,
                "evidence_count": 1,
            }],
        }

        assert learner.observe(experience) is None
        promoted = learner.observe(experience)

        assert promoted is not None
        assert promoted["evidence_count"] == 2
        assert promoted["status"] == "ACTIVE"


def test_skill_store_persists_and_retrieves():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "skills.jsonl"
        store = SkillStore(str(path))
        store.upsert(__import__("memory.skill_store", fromlist=["Skill"]).Skill(
            skill_id="abc123",
            name="agent planning",
            description="Reusable procedure for planning tasks",
            procedure="Retrieve prior planning cases before execution",
            source_lessons=["planning"],
            evidence_count=2,
            quality=0.9,
            reward=0.9,
            confidence=0.9,
        ))
        reloaded = SkillStore(str(path))
        results = reloaded.search("agent planning", limit=1)
        assert results and results[0]["skill_id"] == "abc123"
