from learning.engine import LearningEngine


def test_learning_engine_records_and_retrieves_lessons():
    engine = LearningEngine()
    engine.observe("browser task", [], ["browser-agent"], True, 0.9, 0.9,
                   lessons=["reuse successful browser workflow"])
    ctx = engine.context("browser task")
    assert ctx["experiences"]
    assert ctx["lessons"]


def test_learning_engine_promotes_only_above_threshold():
    engine = LearningEngine()
    assert not engine.promote_lesson("weak", 0.69)
    assert engine.promote_lesson("strong", 0.70)
