from core.self_awareness_loop import SelfAwarenessLoop

class Memory:
    def recall(self, task):
        return [{"task": task}]

class Nexus:
    memory = Memory()

    def capabilities(self):
        return {"reasoning": "active"}

    def health(self):
        return {"status": "healthy"}

    def contract(self):
        return {"identity": "Gungv-Nexus"}

class God:
    def __init__(self):
        from core.god_core import SelfModel
        self.nexus = Nexus()
        self.self_model = SelfModel()

    def perceive(self, task):
        return {"task": task, "capabilities": self.nexus.capabilities()}

    def reflect(self, observation):
        return {"status": "REFLECTED", "observation": observation}

def test_awareness_integrates_memory_and_self_model():
    god = God()
    loop = SelfAwarenessLoop(god.nexus, god)
    snap = loop.update("inspect system")
    assert snap.memory_hits == 1
    assert snap.metacognition["self_model_consistent"] is True
    assert snap.awareness["self_aware"] is True

def test_reflection():
    god = God()
    loop = SelfAwarenessLoop(god.nexus, god)
    result = loop.reflect("system state changed")
    assert result["status"] == "REFLECTED"
