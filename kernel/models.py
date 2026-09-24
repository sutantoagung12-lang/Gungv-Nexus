from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


def now():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Provenance:
    source: str
    retrieved_at: str = field(default_factory=now)
    method: str = "unknown"
    validation: str = "unvalidated"

@dataclass
class Memory:
    id: str
    content: str
    kind: str = "episodic"
    status: str = "ACTIVE"
    confidence: float = 0.5
    provenance: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)

    def to_dict(self):
        return asdict(self)

    def is_stale(self, days=30):
        try:
            from datetime import datetime, timezone, timedelta
            dt=datetime.fromisoformat(self.updated_at.replace("Z","+00:00"))
            return datetime.now(timezone.utc)-dt > timedelta(days=days)
        except Exception:
            return False

@dataclass
class Task:
    id: str
    goal: str
    status: str = "PENDING"
    dependencies: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    results: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
