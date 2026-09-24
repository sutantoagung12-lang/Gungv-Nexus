from kernel.runtime import NexusRuntime

def test_power_mode_returns_focused_context():
    rt=NexusRuntime(".")
    plan=rt.power_plan("build a safer system","implement memory retrieval")
    assert plan["agents"]
    assert plan["focus"]["budget"] == 8
    assert len(plan["safeguards"]) == 4
