from __future__ import annotations

from time import time


def snapshot(registry, orchestrator, audit=None) -> dict:
    workers = registry.list_workers()
    repositories = registry.list_repositories()
    return {
        "status": "ok",
        "timestamp": time(),
        "repositories": len(repositories),
        "enabled_repositories": sum(1 for r in repositories if r.enabled),
        "workers": len(workers),
        "online_workers": sum(1 for w in workers if w.status == "online"),
        "jobs": len(orchestrator.jobs),
        "audit_events": len(audit.events) if audit else 0,
    }
