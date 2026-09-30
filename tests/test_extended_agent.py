from core.nexus_agent import GungvNexusAgent

def test_extended_control_plane():
    a=GungvNexusAgent()
    assert a.schedule("research",80) > 0
    assert a.recover("temporary failure",0)["recoverable"] is True
    assert a.evaluate("ok","ok",{"source":"test"})["promotion_eligible"] is True
    assert a.checkpoint("cp-1",{"phase":"PLAN"})["id"]=="cp-1"
    assert a.contract()["reasoning"]=="explicit-structured-reasoning"
