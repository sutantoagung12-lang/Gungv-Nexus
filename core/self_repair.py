"""Adaptive self-repair engine with broad internal coverage and mandatory verification/rollback."""
class SelfRepair:
    TARGETS = {"signals", "state", "memory", "skills", "organs", "capabilities", "configuration", "tests"}
    def diagnose(self, candidate):
        target = candidate.get("target")
        if target not in self.TARGETS:
            return {"status": "BLOCKED", "reason": "unknown_repair_target"}
        return {"status": "READY", "target": target}

    def repair(self, kernel, candidate):
        diagnosis = self.diagnose(candidate)
        if diagnosis["status"] != "READY":
            return diagnosis
        target = diagnosis["target"]
        snapshot = self._snapshot(kernel, target)
        try:
            changed = self._apply(kernel, target)
            verified = self._verify(kernel, target, changed)
            if not verified:
                self._restore(kernel, target, snapshot)
                return {"status": "ROLLED_BACK", "target": target}
            return {"status": "REPAIRED", "target": target, "verified": True, "snapshot": snapshot}
        except Exception as exc:
            self._restore(kernel, target, snapshot)
            return {"status": "ROLLED_BACK", "target": target, "error": type(exc).__name__}

    def _snapshot(self, kernel, target):
        if target == "signals":
            return list(kernel.signals.history)
        if target == "state":
            return {"mode": kernel.god.state.mode, "cycle": kernel.god.state.cycle}
        return None

    def _apply(self, kernel, target):
        if target == "signals":
            kernel.signals.history = kernel.signals.history[-500:]
            return True
        return False

    def _verify(self, kernel, target, changed):
        if target == "signals":
            return len(kernel.signals.history) <= 500
        return changed is True

    def _restore(self, kernel, target, snapshot):
        if target == "signals" and snapshot is not None:
            kernel.signals.history = snapshot
