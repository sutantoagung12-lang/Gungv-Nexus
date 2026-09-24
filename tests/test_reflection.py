from intelligence.reflection import reflect
from intelligence.memory_policy import should_promote, should_store


def test_reflection_distills_success():
    r = reflect("research task", {"success": True, "quality": .9, "reward": .8})
    assert r["type"] == "procedural"
    assert r["confidence"] > .5


def test_memory_policy_gates_promotion():
    assert should_store(reward=.7, quality=.8, confidence=.8)
    assert not should_store(reward=.9, quality=.9, confidence=.9, destructive=True)
    assert should_promote(reward=.8, quality=.8, confidence=.8)
