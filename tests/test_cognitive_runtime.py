from kernel.runtime import NexusRuntime

def test_cognitive_runtime_safe_cycle():
    rt = NexusRuntime(".")
    result = rt.cognitive_cycle("improve memory", "analyze memory retrieval")
    assert result["status"] == "EVALUATED"
    assert result["evaluation"]["passed"] is True

def test_cognitive_runtime_gates_destructive_cycle():
    rt = NexusRuntime(".")
    result = rt.cognitive_cycle("clean repository", "delete old data")
    assert result["plan"]["agents"]
    assert result["evaluation"]["passed"] is True
