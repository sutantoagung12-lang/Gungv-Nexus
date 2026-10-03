"""CMRA <-> Gungv-Nexus control-plane contract.

CMRA owns local state integrity, snapshots and rollback. Nexus owns orchestration,
policy, routing and promotion gates. This bridge is intentionally side-effect free:
it prepares requests and validates contracts; it does not execute destructive actions.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

CMRA_RELEASE = "1.0.0"
CMRA_SCHEMA = 3
NEXUS_ARCHITECTURE = "27.0.0"

@dataclass(frozen=True)
class CMRAContract:
    component: str = "CMRA"
    release: str = CMRA_RELEASE
    schema: int = CMRA_SCHEMA
    rollback_release: str = "0.9.0"
    execution: str = "local-state"
    destructive_actions: str = "confirmation-required"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

def build_handshake() -> dict[str, Any]:
    return {
        "protocol": "nexus-cmra/v1",
        "nexus": {"architecture": NEXUS_ARCHITECTURE, "role": "control-plane"},
        "cmra": CMRAContract().as_dict(),
        "capabilities": [
            "state-integrity", "audit-chain", "snapshot", "rollback",
            "import-validation", "runtime-self-test"
        ],
        "execution": {
            "external": False,
            "destructive": False,
            "requires_human_approval": True,
        },
    }

def validate_handshake(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if payload.get("protocol") != "nexus-cmra/v1":
        errors.append("protocol_mismatch")
    cmra = payload.get("cmra") or {}
    if cmra.get("release") != CMRA_RELEASE:
        errors.append("cmra_release_mismatch")
    if cmra.get("schema") != CMRA_SCHEMA:
        errors.append("cmra_schema_mismatch")
    if cmra.get("rollback_release") != "0.9.0":
        errors.append("rollback_baseline_mismatch")
    execution = payload.get("execution") or {}
    if execution.get("external") is not False:
        errors.append("external_execution_must_be_disabled")
    if execution.get("destructive") is not False:
        errors.append("destructive_execution_must_be_disabled")
    if execution.get("requires_human_approval") is not True:
        errors.append("human_approval_gate_missing")
    return not errors, errors

def prepare_state_operation(operation: str, *, snapshot_id: str | None = None) -> dict[str, Any]:
    allowed = {"status", "snapshot", "rollback", "audit", "self-test"}
    if operation not in allowed:
        raise ValueError(f"unsupported CMRA operation: {operation}")
    return {
        "protocol": "nexus-cmra/v1",
        "operation": operation,
        "snapshot_id": snapshot_id,
        "executed": False,
        "approval_required": operation == "rollback",
        "release": CMRA_RELEASE,
    }
