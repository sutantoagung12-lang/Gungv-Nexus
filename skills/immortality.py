"""Continuity / 'immortality' skill for Nexus.

The term means durable system continuity: preserve state, recover from failure,
verify restored state, and evolve without losing validated knowledge.
"""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ImmortalitySkill:
    name: str = "immortality"
    version: str = "1.0.0"
    protected_assets: set[str] = field(default_factory=lambda: {
        "validated_knowledge", "skills", "capabilities", "checkpoints",
        "configuration", "lessons"
    })

    def preserve(self, state: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(state, dict):
            raise TypeError("state must be a dictionary")
        return {"status": "PRESERVED", "state": dict(state), "version": self.version}

    def checkpoint(self, state: dict[str, Any]) -> dict[str, Any]:
        preserved = self.preserve(state)
        preserved["checkpoint"] = True
        return preserved

    def recover(self, checkpoint: dict[str, Any]) -> dict[str, Any]:
        if not checkpoint.get("checkpoint") or "state" not in checkpoint:
            return {"status": "RECOVERY_BLOCKED", "reason": "invalid_checkpoint"}
        return {"status": "RECOVERED", "state": dict(checkpoint["state"]), "verified": True}

    def continuity_check(self, current: dict[str, Any], recovered: dict[str, Any]) -> dict[str, Any]:
        same = current == recovered
        return {"continuous": same, "verified": same}

    def evolve_without_loss(self, baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
        missing = sorted(set(baseline) - set(candidate))
        return {
            "status": "SAFE_TO_PROMOTE" if not missing else "BLOCKED",
            "missing_protected_state": missing,
            "preserves_baseline": not missing,
        }
