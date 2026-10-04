"""CMRA service health/readiness contract."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Mapping

SERVICE_RELEASE = "1.1.0"
REQUIRED_COMPONENTS = ("storage", "runtime", "rollback_guard")

@dataclass(frozen=True)
class HealthReport:
    status: str
    release: str = SERVICE_RELEASE
    checks: dict[str, str] | None = None
    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checks"] = dict(self.checks or {})
        return data

def evaluate_health(checks: Mapping[str, bool]) -> HealthReport:
    normalized = {name: ("ok" if checks.get(name, False) else "failed")
                  for name in REQUIRED_COMPONENTS}
    status = "ok" if all(v == "ok" for v in normalized.values()) else "failed"
    return HealthReport(status=status, checks=normalized)

def readiness(checks: Mapping[str, bool]) -> bool:
    return evaluate_health(checks).status == "ok"
