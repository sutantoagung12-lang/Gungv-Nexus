from __future__ import annotations

from dataclasses import asdict, dataclass
from time import time
from uuid import uuid4


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    action: str
    target: str
    actor: str
    outcome: str
    timestamp: float
    metadata: dict


class AuditLog:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, action: str, target: str, actor: str = "nexus", outcome: str = "accepted", metadata: dict | None = None) -> AuditEvent:
        event = AuditEvent(uuid4().hex, action, target, actor, outcome, time(), metadata or {})
        self.events.append(event)
        return event

    def list(self) -> list[dict]:
        return [asdict(event) for event in self.events]
