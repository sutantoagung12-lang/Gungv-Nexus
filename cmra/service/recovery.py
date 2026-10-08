"""CMRA v1.2 recovery journal with explicit rollback checkpoints."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

SCHEMA_VERSION = 1
ROLLBACK_BASELINE = "0.9.0"

@dataclass(frozen=True)
class Checkpoint:
    checkpoint_id: str
    state_version: int
    state_hash: str
    rollback_target: str = ROLLBACK_BASELINE

class RecoveryJournal:
    def __init__(self) -> None:
        self._checkpoints: list[Checkpoint] = []

    @staticmethod
    def digest(state: Any) -> str:
        payload = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
        return sha256(payload).hexdigest()

    def checkpoint(self, checkpoint_id: str, state_version: int, state: Any) -> Checkpoint:
        if state_version < 1:
            raise ValueError("state_version must be >= 1")
        if self._checkpoints and state_version <= self._checkpoints[-1].state_version:
            raise ValueError("state_version must increase monotonically")
        cp = Checkpoint(checkpoint_id, state_version, self.digest(state))
        self._checkpoints.append(cp)
        return cp

    def latest(self) -> Checkpoint | None:
        return self._checkpoints[-1] if self._checkpoints else None

    def can_rollback(self, target_version: int, approved: bool) -> bool:
        return approved and any(c.state_version == target_version for c in self._checkpoints)
