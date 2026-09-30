from skills.ai_dominance import AIDominanceSkill


def test_ai_dominance_maps_gaps():
    result = AIDominanceSkill().assess(
        ["reasoning", "agents", "memory"],
        ["planning", "retrieval"],
    )
    assert result.status == "CANDIDATE"
    assert "rag" in result.gaps
    assert "security" in result.gaps
    assert "benchmark" in result.actions


def test_ai_dominance_requires_validation():
    rule = AIDominanceSkill.expansion_rule()
    assert "Promote a capability" in rule
    assert "evidence" in rule
