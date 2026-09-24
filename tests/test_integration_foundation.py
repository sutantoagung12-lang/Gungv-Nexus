from cognition.attention import AttentionEngine
from cognition.planning import PlanningEngine
from cognition.decision import DecisionEngine
from confidence.engine import ConfidenceEngine
from contradiction.detector import ContradictionDetector
from federation.crosscheck import cross_check

def test_attention():
    assert AttentionEngine().select(["git","memory"],["memory"])[0]=="memory"

def test_plan():
    assert len(PlanningEngine().plan("x",["a","b"])["steps"])==2

def test_decision_requires_human():
    assert DecisionEngine().prepare("q",["a"])["status"]=="needs-human-decision"

def test_confidence():
    assert ConfidenceEngine().assess(2,2)["level"]=="supported"

def test_contradiction():
    claims=[{"subject":"x","predicate":"p","object":"a"},{"subject":"x","predicate":"p","object":"b"}]
    assert ContradictionDetector().find(claims)

def test_crosscheck():
    assert cross_check("x",["a","b"])["status"]=="validated-candidate"
