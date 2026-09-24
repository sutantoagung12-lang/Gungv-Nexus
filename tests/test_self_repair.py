from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from evolution.self_repair import SelfRepairEngine


def test_repair_requires_all_gates():
    engine = SelfRepairEngine()
    candidate = engine.diagnose({
        "target": "planner",
        "error": "bad plan",
        "suggested_change": "reuse successful case",
        "evidence": ["case-1", "case-2"],
        "confidence": 0.9,
    })
    rejected = engine.validate(candidate, tests_passed=False, regression_free=True)
    assert rejected["status"] == "REJECTED"


def test_repair_can_be_ready_after_validation():
    engine = SelfRepairEngine()
    candidate = engine.diagnose({
        "target": "planner",
        "error": "bad plan",
        "suggested_change": "reuse successful case",
        "evidence": ["case-1", "case-2"],
        "confidence": 0.9,
    })
    approved = engine.validate(candidate, tests_passed=True, regression_free=True)
    assert approved["status"] == "READY_FOR_PROMOTION"
