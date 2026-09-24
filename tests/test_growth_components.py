from kernel.runtime import NexusRuntime
from economics.opportunity import Opportunity

def test_opportunity_engine():
    rt=NexusRuntime(".")
    rows=rt.opportunities([
        Opportunity("digital product",100,20,.1,.8),
        Opportunity("high risk idea",100,20,.9,.8),
    ])
    assert rows[0]["score"] > rows[1]["score"]

def test_research_loop():
    rt=NexusRuntime(".")
    result=rt.research_prepare("find a monetizable product opportunity")
    assert "cross_check" in result["stages"]

def test_checkpoint():
    rt=NexusRuntime(".")
    saved=rt.checkpoint_save("task-1",{"step":1})
    assert rt.checkpoint_load("task-1")["state"]["step"] == 1
