from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OrganismStatus:
    """Compact control-plane view of the CMRA-X organism."""

    service: str
    repositories: int
    workers: int
    jobs: int
    audit_events: int
    federation: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "status": "ok",
            "repositories": self.repositories,
            "workers": self.workers,
            "jobs": self.jobs,
            "audit_events": self.audit_events,
            "federation": self.federation,
        }


def build_organism_status(
    *,
    repositories: int,
    workers: int,
    jobs: int,
    audit_events: int,
    federation: dict[str, Any],
) -> OrganismStatus:
    """Build a read-only aggregate snapshot; never exposes credentials or payloads."""
    return OrganismStatus(
        service="gungv-nexus",
        repositories=max(0, int(repositories)),
        workers=max(0, int(workers)),
        jobs=max(0, int(jobs)),
        audit_events=max(0, int(audit_events)),
        federation=dict(federation),
    )
