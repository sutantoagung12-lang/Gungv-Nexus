from core.god_kernel import GodKernel
from core.homeostasis import Homeostasis
from core.self_diagnosis import SelfDiagnosis
from core.self_repair import SelfRepair

class N:
    def __init__(self):
        self.nervous_system = type("NS", (), {"emit": lambda *a: None})()
    def capabilities(self): return {}
    def health(self): return {"status": "ok"}
    def contract(self): return {}
    def think(self, t): return type("C", (), {"task": t, "stage": "PLAN"})()
    def propose_capability(self, *a): return {}
    def propose_organ(self, *a): return {}

def test_health():
    k = GodKernel(N())
    assert Homeostasis().inspect(k).status == "HEALTHY"

def test_repair_is_bounded():
    assert SelfRepair().repair(None, {"target": "credentials"})["status"] == "BLOCKED"
    assert SelfDiagnosis().diagnose(type("S", (), {"alerts": ["signals"]})())[0]["target"] == "signals"
