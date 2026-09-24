from learning.engine import LearningEngine


def test_learning_engine_integrates_reflection_and_memory_policy():
    engine = LearningEngine()
    result = engine.observe(
        "browser task", [], ["browser-agent"], True, 0.9, 0.9,
        lessons=["reuse successful browser workflow"],
    )
    assert result["memory_stored"] is True
    assert result["lesson_promoted"] is True
    assert result["reflection"]["type"] == "procedural"
    assert result["experience"]["lesson_records"]


def test_learning_engine_blocks_destructive_memory_write():
    engine = LearningEngine()
    result = engine.observe(
        "destructive task", [], ["tool"], True, 1.0, 1.0,
        destructive=True,
    )
    assert result["memory_stored"] is False
    assert result["experience"]["lesson_records"] == []
