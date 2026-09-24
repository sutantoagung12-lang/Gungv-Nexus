from kernel.runtime import NexusRuntime

def test_memory_intelligence():
    rt=NexusRuntime(".")
    result=rt.memory_intelligence()
    assert "records" in result

def test_knowledge_intelligence():
    rt=NexusRuntime(".")
    result=rt.knowledge_intelligence()
    assert "records" in result

def test_change_gate():
    rt=NexusRuntime(".")
    assert rt.change_gate("delete repository")["confirmation_required"] is True

def test_quality_evaluator():
    rt=NexusRuntime(".")
    assert rt.quality_evaluate({"agents":["reviewer"],"context":{},"status":"READY"})["passed"]
