import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from memory.experience_store import Experience, ExperienceStore
from memory.retrieval import ExperienceRetriever


def test_experience_retrieval_prefers_quality():
    store = ExperienceStore()
    store.record(Experience(
        task="build memory retrieval",
        quality=0.95,
        reward=0.9,
        lesson_records=[{"lesson": "Use prior successful retrieval cases", "confidence": 0.9, "evidence_count": 3}],
    ))
    store.record(Experience(
        task="build memory retrieval",
        quality=0.4,
        reward=0.3,
        lesson_records=[{"lesson": "Low quality case", "confidence": 0.4, "evidence_count": 1}],
    ))

    results = ExperienceRetriever(store).rank("build memory retrieval", limit=2)

    assert len(results) == 2
    assert results[0]["quality"] > results[1]["quality"]
    assert results[0]["retrieval_score"] > results[1]["retrieval_score"]


def test_experience_retrieval_returns_relevant_lessons():
    store = ExperienceStore()
    store.record(Experience(
        task="improve agent planning",
        quality=0.9,
        reward=0.9,
        lesson_records=[{"lesson": "Retrieve prior planning cases before execution", "confidence": 0.9, "evidence_count": 2}],
    ))

    lessons = ExperienceRetriever(store).lessons("improve agent planning")

    assert lessons
    assert "planning" in lessons[0]["lesson"].lower()


def test_experience_store_persists_records():
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "experiences.jsonl"
        store = ExperienceStore(path=str(path))
        store.record(Experience(task="persist experience", quality=0.9, reward=0.9))
        reloaded = ExperienceStore(path=str(path))
        assert reloaded.recent(1)[0]["task"] == "persist experience"
