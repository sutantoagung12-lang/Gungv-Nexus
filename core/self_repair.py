"""Self-repair executor limited to reversible internal maintenance."""
class SelfRepair:
    SAFE = {"signals"}
    def repair(self, kernel, candidate):
        if candidate.get("target") not in self.SAFE:
            return {"status": "BLOCKED", "reason": "outside_safe_internal_repair_scope"}
        if candidate.get("target") == "signals":
            kernel.signals.history = kernel.signals.history[-500:]
        return {"status": "REPAIRED", "target": candidate["target"]}
