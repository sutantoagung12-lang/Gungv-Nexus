from intelligence.architecture import IntelligenceCycle
from intelligence.evaluator import evaluate


def test_cycle_selects_high_expected_value_and_gates_risk():
    cycle = IntelligenceCycle("test")
    selected = cycle.select_action([
        {"name": "safe", "expected_value": 0.7, "confidence": 0.8, "risk": 0.1},
        {"name": "risky", "expected_value": 0.9, "confidence": 0.8, "risk": 0.8},
    ])
    assert selected["name"] == "risky"
    assert cycle.requires_review


def test_evaluator_produces_bounded_reward():
    result = evaluate(success=True, quality=1.0, risk=0.0, efficiency=1.0)
    assert 0.0 <= result["reward"] <= 1.0
